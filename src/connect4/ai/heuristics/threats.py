"""Immediate-threat heuristic."""
from __future__ import annotations

from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic


class ThreatHeuristic(Heuristic):
    """Count playable cells (the next open cell of a column) where dropping a disc
    would complete a four for the AI, minus the same for the human.
    Optional extension: also reward non-playable threats on favourable rows."""
    name = "threats"

    def __init__(self, weight: float = 1.0) -> None:
        # TODO
        raise NotImplementedError

    def evaluate(self, board: Board) -> float:
        # TODO
        raise NotImplementedError

    def breakdown(self, board: Board) -> dict[str, float]:
        # TODO
        raise NotImplementedError
