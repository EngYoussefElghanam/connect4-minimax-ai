"""Heuristic 5: weighted sum of the four heuristics. Weights come from config."""
from connect4 import config
from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic
from connect4.ai.heuristics.score_diff import ScoreDifferenceHeuristic
from connect4.ai.heuristics.open_windows import OpenWindowsHeuristic
from connect4.ai.heuristics.positional import PositionalHeuristic
from connect4.ai.heuristics.threats import ThreatHeuristic


class CompositeHeuristic(Heuristic):
    name = "composite"

    def __init__(self, weights: dict[str, float] | None = None, weight: float = 1.0):
        super().__init__(weight)
        self.weights = dict(config.HEURISTIC_WEIGHTS if weights is None else weights)
        self._parts = {
            "score_diff": ScoreDifferenceHeuristic(),
            "open_windows": OpenWindowsHeuristic(),
            "positional": PositionalHeuristic(),
            "threats": ThreatHeuristic(),
        }

    def breakdown(self, board: Board) -> dict[str, float]:
        return {k: self.weight * self.weights[k] * part.evaluate(board)
                for k, part in self._parts.items()}