"""Draws the board and animates falling discs."""
from __future__ import annotations

from typing import Callable

import pygame

from connect4 import config
from connect4.board import Board
from connect4.ui.gui import theme

_COLOURS = {
    config.EMPTY: theme.HOLE,
    config.HUMAN: theme.HUMAN_COLOUR,
    config.AI: theme.AI_COLOUR,
}


class BoardView:
    def __init__(self, origin=theme.BOARD_ORIGIN, cell=theme.CELL,
                 rows=config.ROWS, cols=config.COLS):
        self.origin = origin
        self.cell = cell
        self.rows = rows
        self.cols = cols
        self.radius = cell // 2 - theme.DISC_PADDING

    def column_at(self, pos: tuple[int, int]) -> int | None:
        """Column under the mouse (the strip above the board counts too), else None."""
        x, y = pos
        ox, oy = self.origin
        if not (ox <= x < ox + self.cols * self.cell):
            return None
        if not (oy - self.cell <= y < oy + self.rows * self.cell):
            return None
        return (x - ox) // self.cell

    def _centre(self, row: int, col: int) -> tuple[int, int]:
        ox, oy = self.origin
        return ox + col * self.cell + self.cell // 2, oy + row * self.cell + self.cell // 2

    def draw(self, surface: pygame.Surface, board: Board, hover_col: int | None = None) -> None:
        ox, oy = self.origin
        pygame.draw.rect(
            surface, theme.BOARD_BLUE,
            (ox, oy, self.cols * self.cell, self.rows * self.cell), border_radius=12,
        )
        for r in range(self.rows):
            for c in range(self.cols):
                pygame.draw.circle(surface, _COLOURS[board.get(r, c)], self._centre(r, c), self.radius)
        if hover_col is not None:
            x = ox + hover_col * self.cell + self.cell // 2
            pygame.draw.circle(surface, theme.HUMAN_COLOUR, (x, oy - self.cell // 2), self.radius)

    def animate_drop(self, surface: pygame.Surface, board: Board, col: int, player: int,
                     redraw: Callable[[], None]) -> None:
        """Animate a disc falling into `col`.

        `board` must be the position BEFORE the disc is placed, and `redraw`
        must draw the whole frame for that same position (no display.flip()).
        """
        row = board.next_open_row(col)
        if row is None:
            return
        ox, oy = self.origin
        x = ox + col * self.cell + self.cell // 2
        y = float(oy - self.cell // 2)
        target = self._centre(row, col)[1]
        velocity = 0.0
        clock = pygame.time.Clock()
        while y < target:
            pygame.event.pump()
            velocity += theme.GRAVITY
            y = min(y + velocity, target)
            redraw()
            pygame.draw.circle(surface, _COLOURS[player], (x, int(y)), self.radius)
            pygame.display.flip()
            clock.tick(theme.FPS)
