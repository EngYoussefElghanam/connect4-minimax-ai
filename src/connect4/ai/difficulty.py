"""Difficulty levels and K (search depth) validation."""
from __future__ import annotations

from enum import Enum

from connect4 import config


class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


def k_for_difficulty(difficulty: Difficulty) -> int:
    """Map a difficulty level to its K using config.DIFFICULTY_K."""
    # TODO
    raise NotImplementedError


def validate_k(k: int) -> int:
    """Return k if config.MIN_K <= k <= config.MAX_K and k is an int; otherwise raise ValueError."""
    # TODO
    raise NotImplementedError


def difficulty_from_name(name: str) -> Difficulty:
    """Case-insensitive lookup ('easy', 'Medium', ...). Raises ValueError if unknown."""
    # TODO
    raise NotImplementedError
