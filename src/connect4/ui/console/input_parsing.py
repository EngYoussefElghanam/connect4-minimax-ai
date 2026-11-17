"""Pure string -> value parsers (no input()/print()), so they are easy to unit-test."""
from __future__ import annotations

from connect4.ai.difficulty import Difficulty


def parse_column_input(raw: str, cols: int) -> int:
    """User types 1..cols. Return the 0-based column. Raise ValueError (with a friendly
    message) for non-numbers or out-of-range values. Surrounding whitespace is allowed."""
    # TODO
    raise NotImplementedError


def parse_k_input(raw: str) -> int:
    """Custom K typed by the user. Return a validated int (use ai.difficulty.validate_k).
    Raise ValueError for non-integers or out-of-range values."""
    # TODO
    raise NotImplementedError


def parse_difficulty_choice(raw: str) -> Difficulty | None:
    """Menu choice. '1'/'easy' -> EASY, '2'/'medium' -> MEDIUM, '3'/'hard' -> HARD,
    '4'/'custom' -> None (meaning: ask for a custom K). Case-insensitive.
    Raise ValueError for anything else."""
    # TODO
    raise NotImplementedError
