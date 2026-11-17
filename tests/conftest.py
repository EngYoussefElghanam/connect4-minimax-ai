import pytest

from connect4.board import Board
import sample_boards as sb


@pytest.fixture
def empty_board() -> Board:
    return Board()


@pytest.fixture
def mid_game_board() -> Board:
    return Board.from_strings(sb.MID_GAME)
