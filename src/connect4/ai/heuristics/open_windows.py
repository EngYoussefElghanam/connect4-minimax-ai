"""Heuristic 2: candidate points. A window with discs of only one player
is still completable by that player; more discs = closer to a four."""

from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic, window_counts

# points for a window holding n own discs and no opponent disc
DISC_POINTS = {1: 1, 2: 5, 3: 20}


class OpenWindowsHeuristic(Heuristic):
    name = "open_windows"

    def breakdown(self, board: Board) -> dict[str, float]:
        ai_pts = human_pts = 0
        for _, ai, hu in window_counts(board):
            if hu == 0 and ai in DISC_POINTS:
                ai_pts += DISC_POINTS[ai]
            elif ai == 0 and hu in DISC_POINTS:
                human_pts += DISC_POINTS[hu]
        return {"ai_open_windows": self.weight * ai_pts,
                "human_open_windows": -self.weight * human_pts}