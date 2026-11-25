"""Pure string -> value parsers (no input()/print()), so they are easy to unit-test."""
from __future__ import annotations

from connect4.ai.difficulty import Difficulty, difficulty_from_name, validate_k

# Menu numbers shown by the CLI -> difficulty (None = ask for a custom K).
_MENU = {"1": Difficulty.EASY, "2": Difficulty.MEDIUM, "3": Difficulty.HARD, "4": None}


def parse_column_input(raw: str, cols: int) -> int:
    """User types 1..cols. Return the 0-based column; ValueError otherwise."""
    cleaned = raw.strip()
    try:
        number = int(cleaned)
    except ValueError as exc:
        raise ValueError(f"{cleaned!r} is not a whole number") from exc
    if not 1 <= number <= cols:
        raise ValueError(f"column must be between 1 and {cols}")
    return number - 1


def parse_k_input(raw: str) -> int:
    """Custom K typed by the user; validated as a positive integer."""
    cleaned = raw.strip()
    try:
        k = int(cleaned)
    except ValueError as exc:
        raise ValueError(f"{cleaned!r} is not a whole number") from exc
    return validate_k(k)


def parse_difficulty_choice(raw: str) -> Difficulty | None:
    """'1'/'easy', '2'/'medium', '3'/'hard'; '4'/'custom' -> None (ask for K)."""
    cleaned = raw.strip().lower()
    if cleaned in _MENU:
        return _MENU[cleaned]
    if cleaned == "custom":
        return None
    return difficulty_from_name(cleaned)
