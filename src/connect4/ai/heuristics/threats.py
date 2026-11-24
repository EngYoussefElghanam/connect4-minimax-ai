"""Heuristic 4: a window with 3 own discs + 1 empty cell that is playable NOW."""
from connect4 import config
from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic, window_counts


class ThreatHeuristic(Heuristic):
    name = "threats"

    def breakdown(self, board: Board) -> dict[str, float]:
        ai_t = human_t = 0
        for cells, ai, hu in window_counts(board):
            if not ((ai == 3 and hu == 0) or (hu == 3 and ai == 0)):
                continue
            for r, c in cells:
                if board.get(r, c) == config.EMPTY:
                    if board.next_open_row(c) == r:     # playable now
                        if ai == 3:
                            ai_t += 1
                        else:
                            human_t += 1
                    break
        return {"ai_threats": self.weight * ai_t,
                "human_threats": -self.weight * human_t}