import pytest

from connect4 import config
from connect4.board import Board
from connect4.ai.heuristics import ALL_HEURISTICS, get_heuristic
from connect4.ai.heuristics.composite import CompositeHeuristic
from connect4.ai.heuristics.open_windows import OpenWindowsHeuristic
from connect4.ai.heuristics.positional import PositionalHeuristic
from connect4.ai.heuristics.score_diff import ScoreDifferenceHeuristic
from connect4.ai.heuristics.threats import ThreatHeuristic
import sample_boards as sb


def B(rows):
    return Board.from_strings(rows)


SAMPLES = [sb.MID_GAME, sb.AI_THREE_OPEN, sb.AI_FOUR, sb.BOTH_FOUR, sb.VERTICAL_THREAT, sb.AI_TWO_BLOCKED]


# ---------------------------------------------------------------- contract for ALL heuristics
@pytest.fixture(params=sorted(ALL_HEURISTICS))
def heuristic(request):
    return get_heuristic(request.param)


def test_registry_unknown_name_raises():
    with pytest.raises(ValueError):
        get_heuristic("does_not_exist")


def test_registry_contains_composite():
    assert "composite" in ALL_HEURISTICS


def test_returns_a_number(heuristic):
    assert isinstance(heuristic.evaluate(B(sb.MID_GAME)), (int, float))


def test_empty_board_is_zero(heuristic, empty_board):
    assert heuristic.evaluate(empty_board) == pytest.approx(0)


@pytest.mark.parametrize("rows", SAMPLES)
def test_antisymmetric_under_player_swap(heuristic, rows):
    b = B(rows)
    assert heuristic.evaluate(b) == pytest.approx(-heuristic.evaluate(b.swapped()))


@pytest.mark.parametrize("rows", SAMPLES)
def test_breakdown_sums_to_evaluate(heuristic, rows):
    b = B(rows)
    assert sum(heuristic.breakdown(b).values()) == pytest.approx(heuristic.evaluate(b))


def test_evaluate_does_not_mutate_board(heuristic):
    b = B(sb.MID_GAME)
    heuristic.evaluate(b)
    heuristic.breakdown(b)
    assert b.to_strings() == sb.MID_GAME


def test_computer_ahead_is_never_worse_than_human_ahead(heuristic):
    assert heuristic.evaluate(B(sb.AI_FOUR)) >= heuristic.evaluate(B(sb.HUMAN_FOUR))


# ---------------------------------------------------------------- ScoreDifference
class TestScoreDifference:
    @pytest.fixture
    def h(self):
        return ScoreDifferenceHeuristic()

    def test_sign(self, h):
        assert h.evaluate(B(sb.AI_FOUR)) > 0
        assert h.evaluate(B(sb.HUMAN_FOUR)) < 0
        assert h.evaluate(B(sb.BOTH_FOUR)) == 0

    def test_more_fours_is_better(self, h):
        assert h.evaluate(B(sb.AI_FIVE)) > h.evaluate(B(sb.AI_FOUR))

    def test_weight_scales_value(self, h):
        assert ScoreDifferenceHeuristic(weight=3.0).evaluate(B(sb.AI_FOUR)) == pytest.approx(3.0)


# ---------------------------------------------------------------- OpenWindows (candidate points)
class TestOpenWindows:
    @pytest.fixture
    def h(self):
        return OpenWindowsHeuristic()

    def test_more_discs_in_open_windows_is_better(self, h):
        assert h.evaluate(B(sb.AI_THREE_OPEN)) > h.evaluate(B(sb.AI_TWO)) \
               > h.evaluate(B(sb.AI_ONE)) > 0

    def test_opponent_disc_kills_windows(self, h):
        assert h.evaluate(B(sb.AI_TWO_BLOCKED)) < h.evaluate(B(sb.AI_TWO))

    def test_human_open_three_is_negative(self, h):
        assert h.evaluate(B(sb.HUMAN_THREE_OPEN)) < 0


# ---------------------------------------------------------------- Positional
class TestPositional:
    @pytest.fixture
    def h(self):
        return PositionalHeuristic()

    def test_centre_beats_edge(self, h):
        assert h.evaluate(B(sb.A_CENTRE)) > h.evaluate(B(sb.A_EDGE))
        assert h.evaluate(B(sb.A_CENTRE)) > 0

    def test_human_centre_is_worse_for_ai(self, h):
        assert h.evaluate(B(sb.H_CENTRE)) < h.evaluate(B(sb.H_EDGE)) <= 0


# ---------------------------------------------------------------- Threats
class TestThreats:
    @pytest.fixture
    def h(self):
        return ThreatHeuristic()

    def test_playable_winning_cell_counts(self, h):
        assert h.evaluate(B(sb.AI_THREE_OPEN)) > 0
        assert h.evaluate(B(sb.HUMAN_THREE_OPEN)) < 0

    def test_blocked_three_is_not_a_threat(self, h):
        assert h.evaluate(B(sb.AI_THREE_BLOCKED)) == 0

    def test_vertical_threat_is_seen(self, h):
        assert h.evaluate(B(sb.VERTICAL_THREAT)) < 0


# ---------------------------------------------------------------- Composite
class TestComposite:
    def test_breakdown_keys_match_config(self, mid_game_board):
        assert set(CompositeHeuristic().breakdown(mid_game_board)) == set(config.HEURISTIC_WEIGHTS)

    def test_custom_weights_are_used(self):
        h = CompositeHeuristic(weights={"score_diff": 2.0, "open_windows": 0,
                                        "positional": 0, "threats": 0})
        assert h.evaluate(B(sb.AI_FOUR)) == pytest.approx(2.0)

    def test_sign(self):
        h = CompositeHeuristic()
        assert h.evaluate(B(sb.AI_FOUR)) > 0
        assert h.evaluate(B(sb.HUMAN_THREE_OPEN)) < 0
