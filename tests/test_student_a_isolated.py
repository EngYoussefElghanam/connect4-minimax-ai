"""Student A tests that run BEFORE teammates implement the heuristic modules.

Uses a minimal test-only score-difference heuristic. This is NOT the team's
production heuristic or an implementation of a teammate's responsibilities.
"""
import pytest

from connect4 import config
from connect4.board import Board
from connect4.scoring import get_scores, score_difference
from connect4.ai.heuristics.base import Heuristic
from connect4.ai.minimax import MinimaxAgent
from connect4.ai.stats import SearchStats
from connect4.ai.tree import count_nodes, iter_nodes
from connect4.game import Game
import sample_boards as sb
from benchmarks import k_analysis


class SimpleScoreDifference(Heuristic):
    name = "test_score_difference"

    def evaluate(self, board):
        return float(score_difference(board))

    def breakdown(self, board):
        return {"score_diff": self.evaluate(board)}


@pytest.fixture
def score_heuristic():
    return SimpleScoreDifference()


def test_search_preserves_board_and_chooses_immediate_point(score_heuristic):
    board = Board.from_strings(sb.AI_THREE_OPEN)
    before = board.to_strings()
    result = MinimaxAgent(score_heuristic, 1).choose_move(board)
    assert result.column in (0, 4)
    assert result.value == pytest.approx(1)
    assert board.to_strings() == before
    assert result.stats.nodes_expanded == 8
    assert result.stats.leaf_evaluations == 7


def test_search_blocks_opponent_threat(score_heuristic):
    result = MinimaxAgent(score_heuristic, 2).choose_move(Board.from_strings(sb.VERTICAL_THREAT))
    assert result.column == 3
    assert result.value == 0


def test_full_board_is_terminal_not_first_four(score_heuristic):
    game = Game(2, score_heuristic, board=Board.from_strings(sb.AI_FOUR))
    assert not game.is_over()
    assert get_scores(game.board) == (0, 1)
    with pytest.raises(ValueError):
        game.result()


def test_equivalent_value_and_reduced_nodes_with_pruning(score_heuristic):
    board = Board.from_strings(sb.MID_GAME)
    values = {}
    for k in (1, 2, 3, 4):
        plain = MinimaxAgent(score_heuristic, k, use_pruning=False).choose_move(board)
        pruned = MinimaxAgent(score_heuristic, k, use_pruning=True).choose_move(board)
        assert pruned.value == pytest.approx(plain.value)
        assert pruned.stats.nodes_expanded <= plain.stats.nodes_expanded
        assert count_nodes(pruned.tree, include_pruned=False) == pruned.stats.nodes_expanded
        assert all(n.value is None and not n.children for n in iter_nodes(pruned.tree) if n.pruned)
        values[k] = pruned.value
    assert plain.stats.prunes == 0
    assert pruned.stats.prunes > 0


def test_unpruned_7_way_tree_at_depth_two(score_heuristic):
    result = MinimaxAgent(score_heuristic, 2, use_pruning=False).choose_move(Board())
    assert result.stats.nodes_expanded == 1 + 7 + 49
    assert result.stats.leaf_evaluations == 49
    assert count_nodes(result.tree) == 57
    leaves = [n for n in iter_nodes(result.tree) if n.is_leaf]
    assert len(leaves) == 49
    assert all(n.board is not None and n.heuristic_breakdown is not None for n in leaves)


def test_game_cycle_and_full_board_result(score_heuristic):
    game = Game(2, score_heuristic)
    game.human_move(3)
    reply = game.computer_move()
    assert reply.column in range(7)
    assert game.board.count_pieces() == 2
    assert game.current_player == config.HUMAN
    final = Game(1, score_heuristic, Board.from_strings(sb.FULL_AI_WINS))
    assert final.is_over()
    assert final.result().ai_score == 2
    assert final.result().human_score == 1


def test_benchmark_with_test_only_heuristic(monkeypatch, score_heuristic, tmp_path):
    monkeypatch.setattr(k_analysis, "get_heuristic", lambda name: score_heuristic)
    positions = k_analysis.sample_positions()
    assert len(positions) == 4
    assert [p.count_pieces() for p in positions] == [0, 4, 12, 26]
    rows = k_analysis.run_k_analysis([1, 2], "test_score_difference", [Board()])
    assert len(rows) == 4
    assert set(rows[0]) == set(k_analysis.FIELDS)
    assert all(row["time_seconds"] >= 0 for row in rows)
    path = tmp_path / "k.csv"
    k_analysis.write_csv(rows, str(path))
    assert path.is_file()


def test_stats_reset():
    stats = SearchStats(5, 4, 3, 2.0, 1)
    stats.reset()
    assert all(x == 0 for x in vars(stats).values())
