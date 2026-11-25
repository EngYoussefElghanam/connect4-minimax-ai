"""pygame front end. Run with:  python main.py --gui"""
from __future__ import annotations

import pygame

from connect4 import config
from connect4.ai.heuristics import get_heuristic
from connect4.board import Board
from connect4.game import Game
from connect4.scoring import get_scores
from connect4.ui.gui import theme
from connect4.ui.gui.board_view import BoardView
from connect4.ui.gui.menu_view import MenuView
from connect4.ui.gui.tree_view import TreeView
from connect4.ui.console.cli import print_computer_turn


class _GuiApp:
    def __init__(self, k: int | None, heuristic_name: str | None, human_starts: bool,
                 use_pruning: bool = True):
        pygame.init()
        pygame.display.set_caption("Connect 4 - Minimax")
        desktop_w, desktop_h = pygame.display.get_desktop_sizes()[0]
        scale = min(1, desktop_w * .94 / theme.WINDOW_W, desktop_h * .90 / theme.WINDOW_H)
        self.window = pygame.display.set_mode((int(theme.WINDOW_W * scale), int(theme.WINDOW_H * scale)),
                                              pygame.RESIZABLE)
        self.screen = pygame.Surface((theme.WINDOW_W, theme.WINDOW_H))
        self.menu_button = pygame.Rect(1034, 32, 112, 44)
        self.clock = pygame.time.Clock()
        self.human_starts = human_starts
        self.use_pruning = use_pruning

        self.font = pygame.font.Font(theme.FONT_NAME, theme.FONT_MEDIUM)
        self.small = pygame.font.Font(theme.FONT_NAME, theme.FONT_SMALL)
        self.big = pygame.font.Font(theme.FONT_NAME, theme.FONT_LARGE)
        tree_font = pygame.font.SysFont(theme.TREE_FONT_NAMES, theme.TREE_FONT_SIZE)

        self.menu = MenuView(k, heuristic_name)
        self.board_view = BoardView()
        self.tree_view = TreeView(theme.TREE_RECT, tree_font)
        self.game: Game | None = None
        self.state = "menu"          # "menu" | "play" | "over"
        self.status = ""

        if k is not None and heuristic_name is not None:
            self.start_game(k, heuristic_name)

    # ---- game flow -----------------------------------------------------
    def start_game(self, k: int, heuristic_name: str) -> None:
        self.game = Game(k, get_heuristic(heuristic_name), human_starts=self.human_starts,
                         use_pruning=self.use_pruning)
        human, ai = theme.HUMAN_COLOUR, theme.AI_COLOUR
        if not self.menu.human_red:
            human, ai = ai, human
        self.board_view.colours.update({config.HUMAN: human, config.AI: ai})
        self.tree_view.colours = self.board_view.colours
        self.tree_view.set_tree(None)
        self.state = "play"
        self.status = "Choose a column to drop your piece."

    def _after_move(self) -> None:
        if self.game.is_over():
            self.state = "over"

    def _human_click(self, pos) -> None:
        col = self.board_view.column_at(pos)
        if col is None:
            return
        if not self.game.board.is_valid_move(col):
            self.status = "That column is full."
            return
        self.board_view.animate_drop(
            self.screen, self.game.board, col, config.HUMAN,
            lambda: self._draw_frame(self.game.board, hover=False), self._present,
        )
        self.game.human_move(col)
        self.status = "Computer's turn."
        self._after_move()

    def _ai_turn(self) -> None:
        self.status = "Computer is thinking..."
        self._draw_frame(self.game.board)
        self._present()
        before = self.game.board.copy()
        result = self.game.computer_move()          # blocks while searching
        print_computer_turn(self.game, result)  # mandatory terminal trace on every AI turn
        self.board_view.animate_drop(
            self.screen, before, result.column, config.AI,
            lambda: self._draw_frame(before, hover=False), self._present,
        )
        self.tree_view.set_tree(result.tree)
        s = result.stats
        self.status = (f"Computer played column {result.column + 1} | "
                       f"nodes {s.nodes_expanded}, prunes {s.prunes}, {s.elapsed_seconds:.2f}s")
        self._after_move()

    # ---- drawing -------------------------------------------------------
    def _draw_frame(self, board: Board, hover: bool = True) -> None:
        self.screen.fill(theme.BG)
        if self.state == "menu":
            self.menu.draw(self.screen)
            return
        human, ai = get_scores(board)
        self.screen.blit(self.big.render("Connect Four", True, theme.TEXT), (44, 34))
        for x, label, score, player in ((354, "You", human, config.HUMAN),
                                        (540, "Computer", ai, config.AI)):
            pygame.draw.circle(self.screen, self.board_view.colours[player], (x, 54), 12)
            self.screen.blit(self.font.render(f"{label}   {score}", True, theme.TEXT), (x+21, 45))
        pygame.draw.rect(self.screen, theme.PANEL, self.menu_button, border_radius=9)
        menu = self.font.render("Menu", True, theme.TEXT)
        self.screen.blit(menu, menu.get_rect(center=self.menu_button.center))
        pygame.draw.line(self.screen, theme.EDGE, (34, 93), (1146, 93), 2)

        hover_col = None
        if hover and self.state == "play" and self.game.current_player == config.HUMAN:
            hover_col = self.board_view.column_at(self._point(pygame.mouse.get_pos()))
        self.board_view.draw(self.screen, board, hover_col)
        self.tree_view.draw(self.screen)

        if self.state == "over":
            winner = self.game.result().winner
            text = "You win!" if winner == config.HUMAN else "Computer wins" if winner == config.AI else "Draw"
            self.screen.blit(self.font.render(text, True, theme.TEXT), (44, 647))
            self.screen.blit(self.small.render("Press R to play again", True, theme.TEXT_DIM), (44, 673))
        else:
            self.screen.blit(self.font.render("Your move" if self.game.current_player == config.HUMAN
                                              else "Computer's turn", True, theme.TEXT), (44, 645))
            self.screen.blit(self.small.render(self.status, True, theme.TEXT_DIM), (44, 673))

    def _viewport(self):
        return self.screen.get_rect().fit(self.window.get_rect())

    def _point(self, pos):
        rect = self._viewport()
        return ((pos[0] - rect.x) * theme.WINDOW_W // max(1, rect.w),
                (pos[1] - rect.y) * theme.WINDOW_H // max(1, rect.h))

    def _present(self):
        rect = self._viewport()
        self.window.fill(theme.TEXT)
        if rect.size == self.screen.get_size():
            self.window.blit(self.screen, rect)
        elif rect.w and rect.h:
            self.window.blit(pygame.transform.smoothscale(self.screen, rect.size), rect)
        pygame.display.flip()

    # ---- main loop -----------------------------------------------------
    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if hasattr(event, "pos"):
                    event = pygame.event.Event(event.type, dict(event.dict, pos=self._point(event.pos)))
                if event.type == pygame.QUIT:
                    running = False
                elif self.state == "menu":
                    if self.menu.handle_event(event):
                        self.start_game(self.menu.selected_k(), self.menu.selected_heuristic())
                else:
                    self.tree_view.handle_event(event, self._point(pygame.mouse.get_pos()))
                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_r, pygame.K_ESCAPE):
                        self.state = "menu"
                    elif (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                          and self.menu_button.collidepoint(event.pos)):
                        self.state = "menu"
                    elif (self.state == "play" and event.type == pygame.MOUSEBUTTONDOWN
                          and event.button == 1 and self.game.current_player == config.HUMAN):
                        self._human_click(event.pos)

            if not running:
                break
            if (self.state == "play" and not self.game.is_over()
                    and self.game.current_player == config.AI):
                self._ai_turn()

            self._draw_frame(self.game.board if self.game else Board())
            self._present()
            self.clock.tick(theme.FPS)
        pygame.quit()


def run_gui(k: int | None = None, heuristic_name: str | None = None,
            human_starts: bool = True, use_pruning: bool = True) -> None:
    """Open the window. If both k and heuristic_name are given, skip the menu."""
    _GuiApp(k, heuristic_name, human_starts, use_pruning).run()
