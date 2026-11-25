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
        self.colours = dict(_COLOURS)
        self.font = pygame.font.Font(None, 21)

    def column_at(self, pos: tuple[int, int]) -> int | None:
        """Column under the mouse (the strip above the board counts too), else None."""
        x, y = pos
        ox, oy = self.origin
        if not (ox <= x < ox + self.cols * self.cell):
            return None
        if not (oy - 39 <= y < oy + self.rows * self.cell):
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
        for c in range(self.cols):
            x = self._centre(0, c)[0]
            selected = hover_col == c and board.is_valid_move(c)
            if selected:
                pygame.draw.rect(surface, self.colours[config.HUMAN],
                                 (x - 17, oy - 36, 34, 28), border_radius=10)
            number = self.font.render(str(c + 1), True, theme.TEXT)
            surface.blit(number, number.get_rect(center=(x, oy - 22)))
            for r in range(self.rows):
                center = self._centre(r, c)
                player = board.get(r, c)
                pygame.draw.circle(surface, theme.HOLE, center, self.radius)
                if player != config.EMPTY:
                    self._disc(surface, center, player)

    def _disc(self, surface, center, player):
        colour = self.colours[player]
        pygame.draw.circle(surface, colour, center, self.radius - 3)
        ring = tuple(int(channel * .79) for channel in colour)
        pygame.draw.circle(surface, ring, center, self.radius - 10, 2)

    def animate_drop(self, surface: pygame.Surface, board: Board, col: int, player: int,
                     redraw: Callable[[], None], present=pygame.display.flip) -> None:
        """Animate a disc falling into `col`.

        `board` must be the position BEFORE the disc is placed, and `redraw`
        must draw the whole frame for that same position (no display.flip()).
        """
        row = board.next_open_row(col)
        if row is None:
            return
        ox, oy = self.origin
        x = ox + col * self.cell + self.cell // 2
        y = float(oy - 14)
        target = self._centre(row, col)[1]
        velocity = 0.0
        clock = pygame.time.Clock()
        while y < target:
            pygame.event.pump()
            velocity += theme.GRAVITY
            y = min(y + velocity, target)
            redraw()
            self._disc(surface, (x, int(y)), player)
            present()
            clock.tick(theme.FPS)
