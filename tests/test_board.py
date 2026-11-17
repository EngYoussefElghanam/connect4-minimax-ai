import pytest

from connect4 import config
from connect4.board import Board
import sample_boards as sb


def test_new_board_is_empty_with_default_size(empty_board):
    assert (empty_board.rows, empty_board.cols) == (config.ROWS, config.COLS)
    assert empty_board.count_pieces() == 0
    assert empty_board.to_strings() == sb.EMPTY


def test_assignment_minimum_dimensions():
    assert config.COLS >= 7 and config.ROWS >= 6


def test_from_strings_roundtrip():
    assert Board.from_strings(sb.MID_GAME).to_strings() == sb.MID_GAME


def test_from_strings_rejects_ragged_rows():
    with pytest.raises(ValueError):
        Board.from_strings(["...", "..", "..."])


def test_from_strings_rejects_bad_characters():
    with pytest.raises(ValueError):
        Board.from_strings(["..X...."] * 6)


def test_disc_falls_to_bottom(empty_board):
    row = empty_board.drop_piece(3, config.HUMAN)
    assert row == config.ROWS - 1
    assert empty_board.get(config.ROWS - 1, 3) == config.HUMAN


def test_discs_stack(empty_board):
    empty_board.drop_piece(2, config.HUMAN)
    row = empty_board.drop_piece(2, config.AI)
    assert row == config.ROWS - 2
    assert empty_board.get(config.ROWS - 2, 2) == config.AI


def test_column_fills_up_then_rejects(empty_board):
    for _ in range(config.ROWS):
        empty_board.drop_piece(0, config.HUMAN)
    assert not empty_board.is_valid_move(0)
    assert empty_board.next_open_row(0) is None
    assert 0 not in empty_board.valid_moves()
    with pytest.raises(ValueError):
        empty_board.drop_piece(0, config.AI)


@pytest.mark.parametrize("col", [-1, config.COLS, config.COLS + 5])
def test_out_of_range_columns_invalid(empty_board, col):
    assert not empty_board.is_valid_move(col)
    with pytest.raises(ValueError):
        empty_board.drop_piece(col, config.HUMAN)


def test_valid_moves_ascending(empty_board):
    assert empty_board.valid_moves() == list(range(config.COLS))


def test_next_open_row(empty_board):
    assert empty_board.next_open_row(4) == config.ROWS - 1
    empty_board.drop_piece(4, config.AI)
    assert empty_board.next_open_row(4) == config.ROWS - 2


def test_is_full():
    assert Board.from_strings(sb.FULL_DRAW).is_full()
    assert not Board.from_strings(sb.MID_GAME).is_full()


def test_count_pieces(mid_game_board):
    assert mid_game_board.count_pieces() == 8
    assert mid_game_board.count_pieces(config.AI) == 4
    assert mid_game_board.count_pieces(config.HUMAN) == 4


def test_copy_is_independent(mid_game_board):
    clone = mid_game_board.copy()
    clone.drop_piece(0, config.AI)
    assert mid_game_board.count_pieces() == 8
    assert clone.count_pieces() == 9


def test_with_move_leaves_original_untouched(mid_game_board):
    child = mid_game_board.with_move(6, config.AI)
    assert mid_game_board.count_pieces() == 8
    assert child.count_pieces() == 9
    assert child.get(config.ROWS - 1, 6) == config.AI


def test_swapped_exchanges_players():
    b = Board.from_strings(sb.AI_THREE_OPEN)
    assert b.swapped().to_strings() == sb.HUMAN_THREE_OPEN


def test_equality_and_hash(mid_game_board):
    other = Board.from_strings(sb.MID_GAME)
    assert mid_game_board == other
    assert hash(mid_game_board) == hash(other)
    other.drop_piece(0, config.AI)
    assert mid_game_board != other
