"""Draws the board, hover preview, scores, last move, and animates dropping discs."""
from __future__ import annotations

from connect4.board import Board


class BoardView:
    def __init__(self, screen) -> None:
        # TODO
        raise NotImplementedError

    def column_at(self, mouse_x: int) -> int | None:
        """Map a mouse x-position to a 0-based column, or None if outside the board."""
        # TODO
        raise NotImplementedError

    def draw(self, board: Board, hover_col: int | None, scores: tuple[int, int]) -> None:
        # TODO
        raise NotImplementedError

    def animate_drop(self, col: int, row: int, player: int) -> None:
        # TODO (optional polish)
        raise NotImplementedError
