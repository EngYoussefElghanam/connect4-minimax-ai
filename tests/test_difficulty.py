import pytest

from connect4 import config
from connect4.ai.difficulty import (Difficulty, difficulty_from_name,
                                    k_for_difficulty, validate_k)


def test_k_increases_with_difficulty():
    easy, medium, hard = (k_for_difficulty(d) for d in
                          (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD))
    assert easy < medium < hard


@pytest.mark.parametrize("d", list(Difficulty))
def test_difficulty_k_is_within_bounds(d):
    assert config.MIN_K <= k_for_difficulty(d)


def test_validate_k_accepts_bounds():
    assert validate_k(config.MIN_K) == config.MIN_K
    assert validate_k(1000) == 1000


@pytest.mark.parametrize("bad", [0, -3, 2.5])
def test_validate_k_rejects_bad_values(bad):
    with pytest.raises(ValueError):
        validate_k(bad)


def test_validate_k_accepts_above_old_max():
    assert validate_k(11) == 11


@pytest.mark.parametrize("name,expected", [("easy", Difficulty.EASY), ("Medium", Difficulty.MEDIUM),
                                           ("HARD", Difficulty.HARD)])
def test_difficulty_from_name(name, expected):
    assert difficulty_from_name(name) is expected


def test_difficulty_from_name_unknown():
    with pytest.raises(ValueError):
        difficulty_from_name("impossible")
