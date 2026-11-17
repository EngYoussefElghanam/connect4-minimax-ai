"""Candidate-points heuristic."""
from __future__ import annotations

from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic


class OpenWindowsHeuristic(Heuristic):
    """For every 4-cell window containing discs of ONE player only (rest empty),
    add a value that grows with the number of discs (1, 2, 3). Windows containing
    both players' discs are dead and count for nobody. AI windows add, human windows subtract."""
    name = "open_windows"

    def __init__(self, weight: float = 1.0, window_values: tuple[float, float, float] = (1, 4, 16)) -> None:
        # TODO: store weight and the value of a window holding 1 / 2 / 3 discs
        raise NotImplementedError

    def evaluate(self, board: Board) -> float:
        # TODO
        raise NotImplementedError

    def breakdown(self, board: Board) -> dict[str, float]:
        # TODO
        raise NotImplementedError
