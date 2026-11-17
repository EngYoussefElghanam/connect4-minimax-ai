"""Baseline heuristic: current score difference."""
from __future__ import annotations

from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic


class ScoreDifferenceHeuristic(Heuristic):
    """(AI connected-fours) - (human connected-fours), scaled by a weight."""
    name = "score_diff"

    def __init__(self, weight: float = 1.0) -> None:
        # TODO
        raise NotImplementedError

    def evaluate(self, board: Board) -> float:
        # TODO
        raise NotImplementedError

    def breakdown(self, board: Board) -> dict[str, float]:
        # TODO
        raise NotImplementedError
