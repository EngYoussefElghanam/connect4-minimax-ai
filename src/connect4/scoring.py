"""Connected-four counting and final result.

Rule used by the tests: EVERY window of 4 consecutive cells (horizontal, vertical,
both diagonals) fully owned by one player counts as one four. Overlaps count
separately, so 5 in a row = 2 fours.
"""
from __future__ import annotations

from connect4.board import Board


def count_connect_fours(board: Board, player: int) -> int:
    """Number of connected-fours owned by `player`."""
    # TODO: scan the 4 directions
    raise NotImplementedError


def get_scores(board: Board) -> tuple[int, int]:
    """(human_score, ai_score)."""
    # TODO
    raise NotImplementedError


def score_difference(board: Board) -> int:
    """ai_score - human_score (positive = computer ahead)."""
    # TODO
    raise NotImplementedError


def winner(board: Board) -> int | None:
    """HUMAN, AI, or None for a tie. Meant to be used once the board is full,
    but must also work on partial boards (current leader)."""
    # TODO
    raise NotImplementedError


def iter_windows(board: Board):
    """Yield every 4-cell window as a list of (row, col) coordinates.
    Shared by scoring and heuristics so the geometry lives in ONE place."""
    # TODO
    raise NotImplementedError
