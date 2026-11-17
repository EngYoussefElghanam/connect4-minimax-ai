"""Positional (centre-control) heuristic."""
from __future__ import annotations

from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic


class PositionalHeuristic(Heuristic):
    """Sum of per-cell weights for AI discs minus the same for human discs.
    Centre columns weigh more because they take part in more possible fours."""
    name = "positional"

    def __init__(self, weight: float = 1.0) -> None:
        # TODO: build (or compute lazily) the weight table for the board size
        raise NotImplementedError

    def evaluate(self, board: Board) -> float:
        # TODO
        raise NotImplementedError

    def breakdown(self, board: Board) -> dict[str, float]:
        # TODO
        raise NotImplementedError
