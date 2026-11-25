"""Search depth choices and input validation."""

from enum import Enum

from connect4 import config


class Difficulty(Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


def validate_k(k: int) -> int:
    if type(k) is not int or k < config.MIN_K:
        raise ValueError(f"K must be an integer >= {config.MIN_K}")
    return k


def k_for_difficulty(difficulty: Difficulty) -> int:
    if not isinstance(difficulty, Difficulty):
        raise ValueError("difficulty must be a Difficulty enum")
    return validate_k(config.DIFFICULTY_K[difficulty.value])


def difficulty_from_name(name: str) -> Difficulty:
    if not isinstance(name, str):
        raise ValueError("difficulty name must be a string")
    try:
        return Difficulty[name.strip().upper()]
    except KeyError as exc:
        raise ValueError(f"unknown difficulty: {name!r}") from exc
