"""Weighted combination of the individual heuristics — the one you submit for the bonus."""
from __future__ import annotations

from connect4 import config
from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic


class CompositeHeuristic(Heuristic):
    name = "composite"

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        """weights keys: score_diff, open_windows, positional, threats (default: config.HEURISTIC_WEIGHTS)."""
        # TODO: instantiate the sub-heuristics with their weights
        raise NotImplementedError

    def evaluate(self, board: Board) -> float:
        # TODO: sum of the sub-heuristics
        raise NotImplementedError

    def breakdown(self, board: Board) -> dict[str, float]:
        # TODO: {"score_diff": ..., "open_windows": ..., ...} (weighted values)
        raise NotImplementedError
