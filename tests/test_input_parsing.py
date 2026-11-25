import pytest

from connect4 import config
from connect4.ai.difficulty import Difficulty
from connect4.ui.console.input_parsing import (parse_column_input, parse_difficulty_choice,
                                               parse_k_input)


@pytest.mark.parametrize("raw,expected", [("1", 0), ("7", 6), (" 4 ", 3)])
def test_column_is_converted_to_zero_based(raw, expected):
    assert parse_column_input(raw, 7) == expected


@pytest.mark.parametrize("raw", ["0", "8", "-1", "abc", "", "3.5", "  "])
def test_bad_columns_raise(raw):
    with pytest.raises(ValueError):
        parse_column_input(raw, 7)


def test_valid_custom_k():
    assert parse_k_input("3") == 3
    assert parse_k_input(f" {config.MIN_K} ") == config.MIN_K
    assert parse_k_input("1000") == 1000


@pytest.mark.parametrize("raw", ["0", "-1", "abc", "", "2.5"])
def test_bad_custom_k_raises(raw):
    with pytest.raises(ValueError):
        parse_k_input(raw)


@pytest.mark.parametrize("raw,expected", [
    ("1", Difficulty.EASY), ("easy", Difficulty.EASY),
    ("2", Difficulty.MEDIUM), ("Medium", Difficulty.MEDIUM),
    ("3", Difficulty.HARD), ("HARD", Difficulty.HARD),
])
def test_difficulty_choices(raw, expected):
    assert parse_difficulty_choice(raw) is expected


@pytest.mark.parametrize("raw", ["4", "custom", "CUSTOM"])
def test_custom_choice_returns_none(raw):
    assert parse_difficulty_choice(raw) is None


@pytest.mark.parametrize("raw", ["", "9", "nightmare"])
def test_bad_difficulty_choice_raises(raw):
    with pytest.raises(ValueError):
        parse_difficulty_choice(raw)
