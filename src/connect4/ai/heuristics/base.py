"""Heuristic interface.

Sign convention (tests enforce it):
  positive -> computer (AI) better, negative -> human better, 0 -> equal.
Heuristics must be symmetric: evaluate(b) == -evaluate(b.swapped()).
"""
from abc import ABC, abstractmethod

from connect4 import config
from connect4.board import Board
from connect4.scoring import iter_windows


def window_counts(board: Board):
    """Yield (cells, ai_count, human_count) for every 4-cell window."""
    for cells in iter_windows(board):
        values = [board.get(r, c) for r, c in cells]
        yield cells, values.count(config.AI), values.count(config.HUMAN)


class Heuristic(ABC):
    name = "base"

    def __init__(self, weight: float = 1.0):
        self.weight = weight

    @abstractmethod
    def breakdown(self, board: Board) -> dict[str, float]:
        """Per-factor contributions, already weighted."""

    def evaluate(self, board: Board) -> float:
        """Sum of the breakdown, so sum(breakdown) == evaluate by construction."""
        return sum(self.breakdown(board).values())