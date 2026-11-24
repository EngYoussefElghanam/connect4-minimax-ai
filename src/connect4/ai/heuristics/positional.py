"""Heuristic 3: centre columns take part in more windows, so they are worth more."""
from connect4 import config
from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic


class PositionalHeuristic(Heuristic):
    name = "positional"

    def breakdown(self, board: Board) -> dict[str, float]:
        centre = (board.cols - 1) / 2
        ai_pts = human_pts = 0.0
        for r in range(board.rows):
            for c in range(board.cols):
                v = board.get(r, c)
                if v == config.EMPTY:
                    continue
                w = 1 + (centre - abs(c - centre))   # 1 at the edge, max at the centre
                if v == config.AI:
                    ai_pts += w
                else:
                    human_pts += w
        return {"ai_positional": self.weight * ai_pts,
                "human_positional": -self.weight * human_pts}