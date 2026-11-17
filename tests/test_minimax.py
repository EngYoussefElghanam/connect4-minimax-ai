import pytest

from connect4 import config
from connect4.board import Board
from connect4.ai.heuristics.score_diff import ScoreDifferenceHeuristic
from connect4.ai.minimax import MinimaxAgent, SearchResult
from connect4.ai.stats import SearchStats
import sample_boards as sb


def B(rows):
    return Board.from_strings(rows)


def agent(k, **kw):
    return MinimaxAgent(ScoreDifferenceHeuristic(), k=k, **kw)


@pytest.mark.parametrize("bad_k", [0, -1, config.MAX_K + 1])
def test_invalid_k_rejected(bad_k):
    with pytest.raises(ValueError):
        agent(bad_k)


def test_returns_search_result(mid_game_board):
    r = agent(2).choose_move(mid_game_board)
    assert isinstance(r, SearchResult) and isinstance(r.stats, SearchStats)
    assert r.column in mid_game_board.valid_moves()


def test_does_not_mutate_input_board(mid_game_board):
    agent(3).choose_move(mid_game_board)
    assert mid_game_board.to_strings() == sb.MID_GAME


def test_full_board_raises():
    with pytest.raises(ValueError):
        agent(2).choose_move(B(sb.FULL_DRAW))


def test_takes_immediate_scoring_move():
    r = agent(1).choose_move(B(sb.AI_THREE_OPEN))
    assert r.column in (0, 4)          # both complete a four
    assert r.value == pytest.approx(1)


def test_blocks_vertical_threat():
    r = agent(2).choose_move(B(sb.VERTICAL_THREAT))
    assert r.column == 3
    assert r.value == pytest.approx(0)


def test_only_legal_columns_are_chosen():
    rows = ["A......", "H......", "A......", "H......", "A......", "H......"]   # column 0 full
    r = agent(2).choose_move(B(rows))
    assert r.column != 0


def test_single_legal_move_is_returned():
    rows = ["HAHAHA.", "AHAHAH.", "HAHAHA.", "AHAHAH.", "HAHAHA.", "AHAHAH."]
    assert agent(3).choose_move(B(rows)).column == 6


def test_deeper_search_expands_more_nodes(mid_game_board):
    n = [agent(k, use_pruning=False).choose_move(mid_game_board).stats.nodes_expanded for k in (1, 2, 3)]
    assert n[0] < n[1] < n[2]


def test_time_is_recorded(mid_game_board):
    assert agent(2).choose_move(mid_game_board).stats.elapsed_seconds >= 0


def test_root_value_reaches_terminal_utility_on_nearly_full_board():
    # one empty cell left (top of column 6); AI to move, game ends after that disc
    rows = list(sb.FULL_AI_WINS)
    rows[0] = rows[0][:6] + "."
    r = agent(5).choose_move(B(rows))
    assert r.column == 6
