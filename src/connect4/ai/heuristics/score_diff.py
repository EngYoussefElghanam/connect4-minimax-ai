"""Heuristic 1: difference in connected-fours (the real game objective)."""

from connect4 import config
from connect4.board import Board
from connect4.scoring import count_connect_fours
from connect4.ai.heuristics.base import Heuristic


class ScoreDifferenceHeuristic(Heuristic):
    name = "score_diff"

    def breakdown(self, board: Board) -> dict[str, float]:
        diff = (count_connect_fours(board, config.AI)
                - count_connect_fours(board, config.HUMAN))
        return {"score_diff": self.weight * diff}
