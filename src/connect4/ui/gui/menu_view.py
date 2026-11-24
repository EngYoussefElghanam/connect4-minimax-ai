"""Start menu: pick difficulty / K and heuristic, then press Start."""
from __future__ import annotations

import pygame

from connect4 import config
from connect4.ai.difficulty import Difficulty, k_for_difficulty
from connect4.ai.heuristics import ALL_HEURISTICS
from connect4.ui.gui import theme


class _Button:
    def __init__(self, rect: pygame.Rect, label: str):
        self.rect = rect
        self.label = label


class MenuView:
    def __init__(self, k: int | None = None, heuristic: str | None = None):
        pygame.font.init()
        self._title_font = pygame.font.Font(theme.FONT_NAME, theme.FONT_LARGE)
        self._font = pygame.font.Font(theme.FONT_NAME, theme.FONT_MEDIUM)
        self._k = k if k is not None else k_for_difficulty(Difficulty.MEDIUM)
        names = sorted(ALL_HEURISTICS)
        self._heuristic = (heuristic if heuristic in names
                           else "composite" if "composite" in names else names[0])

        cx = theme.WINDOW_W // 2
        self._difficulty_buttons = [
            (_Button(pygame.Rect(cx - 335 + i * 230, 220, 210, 50),
                     f"{d.value.title()} (K={k_for_difficulty(d)})"), d)
            for i, d in enumerate(Difficulty)
        ]
        self._k_minus = _Button(pygame.Rect(cx - 110, 320, 50, 50), "-")
        self._k_plus = _Button(pygame.Rect(cx + 60, 320, 50, 50), "+")
        self._heuristic_buttons = [
            (_Button(pygame.Rect(cx - 290 + (i % 3) * 200, 440 + (i // 3) * 60, 190, 50), name), name)
            for i, name in enumerate(names)
        ]
        self._start = _Button(pygame.Rect(cx - 120, 620, 240, 60), "Start game")

    # ---- public API ----------------------------------------------------
    def selected_k(self) -> int:
        return self._k

    def selected_heuristic(self) -> str:
        """Registry name; the caller turns it into an object with get_heuristic()."""
        return self._heuristic

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Returns True when the Start button was clicked."""
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        for button, difficulty in self._difficulty_buttons:
            if button.rect.collidepoint(event.pos):
                self._k = k_for_difficulty(difficulty)
        if self._k_minus.rect.collidepoint(event.pos):
            self._k = max(config.MIN_K, self._k - 1)
        if self._k_plus.rect.collidepoint(event.pos):
            self._k = min(config.MAX_K, self._k + 1)
        for button, name in self._heuristic_buttons:
            if button.rect.collidepoint(event.pos):
                self._heuristic = name
        return self._start.rect.collidepoint(event.pos)

    def draw(self, surface: pygame.Surface) -> None:
        self._centered(surface, self._title_font, "Connect 4 - Minimax", 90)
        self._centered(surface, self._font, "Difficulty", 185)
        for button, difficulty in self._difficulty_buttons:
            self._draw_button(surface, button, self._k == k_for_difficulty(difficulty))
        self._centered(surface, self._font, f"Search depth K = {self._k}", 290)
        self._draw_button(surface, self._k_minus, False)
        self._draw_button(surface, self._k_plus, False)
        self._centered(surface, self._font, "Heuristic", 405)
        for button, name in self._heuristic_buttons:
            self._draw_button(surface, button, self._heuristic == name)
        self._draw_button(surface, self._start, False)

    # ---- helpers -------------------------------------------------------
    def _centered(self, surface, font, text: str, y: int) -> None:
        img = font.render(text, True, theme.TEXT)
        surface.blit(img, img.get_rect(center=(theme.WINDOW_W // 2, y)))

    def _draw_button(self, surface, button: _Button, selected: bool) -> None:
        hovered = button.rect.collidepoint(pygame.mouse.get_pos())
        colour = theme.BUTTON_SELECTED if selected else (theme.BUTTON_HOVER if hovered else theme.BUTTON)
        pygame.draw.rect(surface, colour, button.rect, border_radius=8)
        label = self._font.render(button.label, True, theme.TEXT)
        surface.blit(label, label.get_rect(center=button.rect.center))
