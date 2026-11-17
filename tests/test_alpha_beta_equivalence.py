"""Alpha-beta must give the SAME root value as plain minimax, just with fewer nodes."""
import pytest

from connect4.board import Board
from connect4.ai.heuristics import ALL_HEURISTICS, get_heuristic
from connect4.ai.minimax import MinimaxAgent
import sample_boards as sb

BOARDS = {"empty": sb.EMPTY, "mid": sb.MID_GAME, "vertical_threat": sb.VERTICAL_THREAT,
          "ai_three": sb.AI_THREE_OPEN}


@pytest.mark.parametrize("heuristic_name", sorted(ALL_HEURISTICS))
@pytest.mark.parametrize("board_name", sorted(BOARDS))
@pytest.mark.parametrize("k", [1, 2, 3, 4])
def test_same_value_with_and_without_pruning(heuristic_name, board_name, k):
    board = Board.from_strings(BOARDS[board_name])
    h = get_heuristic(heuristic_name)
    plain = MinimaxAgent(h, k, use_pruning=False, record_tree=False).choose_move(board)
    pruned = MinimaxAgent(h, k, use_pruning=True, record_tree=False).choose_move(board)
    assert pruned.value == pytest.approx(plain.value)
    assert pruned.stats.nodes_expanded <= plain.stats.nodes_expanded


def test_pruning_strictly_reduces_nodes_at_depth_4():
    h = get_heuristic("composite")
    board = Board.from_strings(sb.MID_GAME)
    plain = MinimaxAgent(h, 4, use_pruning=False, record_tree=False).choose_move(board)
    pruned = MinimaxAgent(h, 4, use_pruning=True, record_tree=False).choose_move(board)
    assert pruned.stats.nodes_expanded < plain.stats.nodes_expanded
    assert pruned.stats.prunes > 0
    assert plain.stats.prunes == 0
