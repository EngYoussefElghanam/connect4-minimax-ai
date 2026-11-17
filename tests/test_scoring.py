import pytest

from connect4 import config
from connect4.board import Board
from connect4.scoring import (count_connect_fours, get_scores, iter_windows,
                              score_difference, winner)
import sample_boards as sb


def B(rows):
    return Board.from_strings(rows)


def test_empty_board_has_no_fours(empty_board):
    assert get_scores(empty_board) == (0, 0)


def test_horizontal_four():
    assert count_connect_fours(B(sb.AI_FOUR), config.AI) == 1
    assert count_connect_fours(B(sb.AI_FOUR), config.HUMAN) == 0


def test_three_is_not_a_four():
    assert count_connect_fours(B(sb.AI_THREE_OPEN), config.AI) == 0


def test_vertical_four():
    rows = ["......."] * 2 + ["H......"] * 4
    assert count_connect_fours(B(rows), config.HUMAN) == 1


def test_diagonal_down_right_four():
    rows = ["A......", ".A.....", "..A....", "...A...", ".......", "......."]
    assert count_connect_fours(B(rows), config.AI) == 1


def test_diagonal_up_right_four():
    rows = [".......", ".......", "...A...", "..A....", ".A.....", "A......"]
    assert count_connect_fours(B(rows), config.AI) == 1


def test_five_in_a_row_counts_two_overlapping_fours():
    assert count_connect_fours(B(sb.AI_FIVE), config.AI) == 2


def test_mixed_colours_do_not_form_a_four():
    assert count_connect_fours(B(_bottom("AAHAA..")), config.AI) == 0


def _bottom(row):
    return ["......."] * 5 + [row]


def test_get_scores_returns_human_then_ai():
    assert get_scores(B(sb.BOTH_FOUR)) == (1, 1)
    assert get_scores(B(sb.FULL_AI_WINS)) == (1, 2)
    assert get_scores(B(sb.FULL_HUMAN_WINS)) == (3, 1)


def test_score_difference_is_ai_minus_human():
    assert score_difference(B(sb.FULL_AI_WINS)) == 1
    assert score_difference(B(sb.FULL_HUMAN_WINS)) == -2
    assert score_difference(B(sb.FULL_DRAW)) == 0


def test_winner_by_greater_number_of_fours():
    assert winner(B(sb.FULL_AI_WINS)) == config.AI
    assert winner(B(sb.FULL_HUMAN_WINS)) == config.HUMAN


def test_winner_tie_is_none():
    assert winner(B(sb.FULL_DRAW)) is None
    assert winner(B(sb.BOTH_FOUR)) is None


def test_iter_windows_total_for_default_board(empty_board):
    # 6x7: 24 horizontal + 21 vertical + 12 + 12 diagonal = 69 windows
    windows = list(iter_windows(empty_board))
    assert len(windows) == 69
    assert all(len(w) == config.CONNECT for w in windows)
