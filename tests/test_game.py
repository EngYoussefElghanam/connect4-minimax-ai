import pytest

from connect4 import config
from connect4.board import Board
from connect4.game import Game, GameResult
from connect4.ai.heuristics.score_diff import ScoreDifferenceHeuristic
from connect4.ai.minimax import SearchResult
import sample_boards as sb


def make_game(**kw):
    kw.setdefault("k", 2)
    kw.setdefault("heuristic", ScoreDifferenceHeuristic())
    return Game(**kw)


def test_invalid_k_rejected():
    with pytest.raises(ValueError):
        make_game(k=0)


def test_human_starts_by_default():
    assert make_game().current_player == config.HUMAN


def test_ai_can_start():
    assert make_game(human_starts=False).current_player == config.AI


def test_human_move_places_disc_and_passes_turn():
    g = make_game()
    row = g.human_move(3)
    assert row == config.ROWS - 1
    assert g.board.get(config.ROWS - 1, 3) == config.HUMAN
    assert g.current_player == config.AI


def test_human_cannot_move_out_of_turn():
    g = make_game()
    g.human_move(0)
    with pytest.raises(ValueError):
        g.human_move(1)


@pytest.mark.parametrize("col", [-1, config.COLS])
def test_illegal_column_rejected(col):
    with pytest.raises(ValueError):
        make_game().human_move(col)


def test_full_column_rejected():
    rows = ["H......", "A......", "H......", "A......", "H......", "A......"]
    g = make_game(board=Board.from_strings(rows))
    with pytest.raises(ValueError):
        g.human_move(0)


def test_computer_move_adds_one_ai_disc_and_returns_search_result():
    g = make_game()
    g.human_move(3)
    r = g.computer_move()
    assert isinstance(r, SearchResult) and r.tree is not None
    assert g.board.count_pieces(config.AI) == 1
    assert g.current_player == config.HUMAN


def test_computer_cannot_move_on_humans_turn():
    with pytest.raises(ValueError):
        make_game().computer_move()


def test_not_over_at_start_and_result_unavailable():
    g = make_game()
    assert not g.is_over()
    with pytest.raises(ValueError):
        g.result()


def test_game_does_not_end_at_first_four():
    rows = ["......."] * 5 + ["AAAA..."]
    g = make_game(board=Board.from_strings(rows))
    assert not g.is_over()


@pytest.mark.parametrize("rows,human,ai,expected", [
    (sb.FULL_DRAW, 0, 0, None),
    (sb.FULL_AI_WINS, 1, 2, config.AI),
    (sb.FULL_HUMAN_WINS, 3, 1, config.HUMAN),
])
def test_final_result(rows, human, ai, expected):
    g = make_game(board=Board.from_strings(rows))
    assert g.is_over()
    assert g.scores() == (human, ai)
    assert g.result() == GameResult(human_score=human, ai_score=ai, winner=expected)


@pytest.mark.timeout(120)
def test_complete_game_runs_until_board_is_full():
    g = make_game(k=2)
    while not g.is_over():
        if g.current_player == config.HUMAN:
            g.human_move(g.board.valid_moves()[0])
        else:
            g.computer_move()
    assert g.board.count_pieces() == config.ROWS * config.COLS
    assert g.result().winner in (config.HUMAN, config.AI, None)
