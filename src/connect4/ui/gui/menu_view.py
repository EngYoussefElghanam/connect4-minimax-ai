"""Start menu: pick difficulty / K and heuristic, then press Start."""
from __future__ import annotations

import pygame

from connect4.ui.gui.art import draw_smiley_disc
from connect4.ai.difficulty import Difficulty, k_for_difficulty, validate_k
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
        self._k_text = str(k if k is not None else k_for_difficulty(Difficulty.MEDIUM))
        self._editing = False
        self._replace = False
        self._error = ""
        self.human_red = True
        names = sorted(ALL_HEURISTICS)
        self._heuristic = (heuristic if heuristic in names
                           else "composite" if "composite" in names else names[0])

        self._display = pygame.font.Font(None, 88)
        self._large = pygame.font.Font(None, 44)
        self._small = pygame.font.Font(None, 22)
        self._difficulty_buttons = [
            (_Button(pygame.Rect(494 + i * 147, 190, 137, 48), d.value.title()), d)
            for i, d in enumerate(Difficulty)
        ]
        self._k_field = pygame.Rect(946, 190, 146, 48)
        self._heuristic_buttons = [
            (_Button(pygame.Rect(494 + i % 3 * 202, 335 + i // 3 * 54, 192, 44),
                     name.replace("_", " ").title()), name)
            for i, name in enumerate(names)
        ]
        self._colour_buttons = [
            (_Button(pygame.Rect(494 + i * 202, 510, 192, 48), label), red)
            for i, (label, red) in enumerate((("Red", True), ("Yellow", False)))
        ]
        self._start = _Button(pygame.Rect(494, 595, 596, 57), "Start game")

    # ---- public API ----------------------------------------------------
    def selected_k(self) -> int:
        return validate_k(int(self._k_text))

    def selected_heuristic(self) -> str:
        """Registry name; the caller turns it into an object with get_heuristic()."""
        return self._heuristic

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Returns True when the Start button was clicked."""
        if event.type == pygame.KEYDOWN and self._editing:
            if event.key == pygame.K_RETURN:
                self._editing = False
                return self._valid_start()
            if event.key == pygame.K_BACKSPACE:
                self._k_text = "" if self._replace else self._k_text[:-1]
                self._replace = False
            elif event.key == pygame.K_a and event.mod & (pygame.KMOD_CTRL | pygame.KMOD_META):
                self._replace = True
            elif event.unicode and event.unicode.isascii() and event.unicode.isdigit():
                self._k_text = event.unicode if self._replace else self._k_text + event.unicode
                self._replace = False
            self._error = ""
            return False
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return False
        self._editing = self._k_field.collidepoint(event.pos)
        self._replace = self._editing
        for button, difficulty in self._difficulty_buttons:
            if button.rect.collidepoint(event.pos):
                self._k_text = str(k_for_difficulty(difficulty))
                self._error = ""
        for button, name in self._heuristic_buttons:
            if button.rect.collidepoint(event.pos):
                self._heuristic = name
        for button, red in self._colour_buttons:
            if button.rect.collidepoint(event.pos):
                self.human_red = red
        return self._start.rect.collidepoint(event.pos) and self._valid_start()

    def _valid_start(self) -> bool:
        try:
            self.selected_k()
        except ValueError:
            self._error = "Enter a positive whole number."
            return False
        self._error = ""
        return True

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(theme.BG)
        ink = theme.TEXT
        def label(font, words, xy, color=ink):
            surface.blit(font.render(words, True, color), xy)

        poster = pygame.Rect(30, 30, 400, 660)
        pygame.draw.rect(surface, theme.BUTTON_SELECTED, poster, border_radius=26)
        label(self._display, "Connect", (62, 64), theme.PANEL)
        label(self._display, "Four", (62, 133), theme.AI_COLOUR)
        # Two standing game pieces share their own illustration area.
        for x, y, radius, color, accessory in (
            (161, 370, 69, theme.HUMAN_COLOUR, "cap"),
            (301, 406, 61, theme.AI_COLOUR, "bow"),
        ):
            for side in (-1, 1):
                foot = (x + side * 28, y + radius + 29)
                pygame.draw.line(surface, theme.PANEL, (x + side * 18, y + radius - 3), foot, 6)
                pygame.draw.line(surface, theme.PANEL, foot, (foot[0] + side * 12, foot[1]), 7)
            draw_smiley_disc(surface, (x, y), radius, color, outline=ink, accessory=accessory)
        label(self._font, "Fill the board.", (64, 564), theme.PANEL)
        label(self._font, "Score the most lines of four.", (64, 593), theme.PANEL)
        pygame.draw.rect(surface, theme.PANEL, (454, 30, 696, 660), border_radius=26)
        label(self._large, "Game setup", (494, 66))
        label(self._font, "Difficulty", (494, 154))
        label(self._font, "Depth (K)", (946, 154))
        for button, difficulty in self._difficulty_buttons:
            self._draw_button(surface, button, self._k_text == str(k_for_difficulty(difficulty)))
        pygame.draw.rect(surface, theme.BUTTON, self._k_field, border_radius=9)
        pygame.draw.rect(surface, theme.BUTTON_SELECTED if self._editing else theme.EDGE,
                         self._k_field, 2, border_radius=9)
        shown = self._k_text[-16:] + ("|" if self._editing else "")
        while self._font.size(shown)[0] > self._k_field.width - 20:
            shown = shown[1:]
        label(self._font, shown, (self._k_field.x + 12, self._k_field.y + 15))
        label(self._small, self._error or "Choose a preset or enter K. Larger depths take longer.",
              (494, 252), (160, 44, 35) if self._error else theme.TEXT_DIM)
        label(self._font, "Evaluation heuristic", (494, 302))
        for button, name in self._heuristic_buttons:
            self._draw_button(surface, button, self._heuristic == name)
        label(self._font, "Your pieces", (494, 475))
        for button, red in self._colour_buttons:
            self._draw_button(surface, button, self.human_red == red)
            pygame.draw.circle(surface, theme.HUMAN_COLOUR if red else theme.AI_COLOUR,
                               (button.rect.left + 22, button.rect.centery), 8)
        self._draw_button(surface, self._start, True)

    def _draw_button(self, surface, button, selected):
        color = theme.BUTTON_SELECTED if selected else theme.BUTTON
        pygame.draw.rect(surface, color, button.rect, border_radius=10)
        if not selected:
            pygame.draw.rect(surface, theme.EDGE, button.rect, 1, border_radius=10)
        label = self._font.render(button.label, True, theme.PANEL if selected else theme.TEXT)
        surface.blit(label, label.get_rect(center=button.rect.center))
