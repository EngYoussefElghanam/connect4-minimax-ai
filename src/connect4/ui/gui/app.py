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


class _GuiApp:
    def __init__(self, k: int | None, heuristic_name: str | None, human_starts: bool,
                 use_pruning: bool = True):
        pygame.init()
        pygame.display.set_caption("Connect 4 - Minimax")
        self.screen = pygame.display.set_mode((theme.WINDOW_W, theme.WINDOW_H))
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
        self.tree_view.set_tree(None)
        self.state = "play"
        self.status = "Your move: click a column."

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
            lambda: self._draw_frame(self.game.board, hover=False),
        )
        self.game.human_move(col)
        self.status = "Computer's turn."
        self._after_move()

    def _ai_turn(self) -> None:
        self.status = "Computer is thinking..."
        self._draw_frame(self.game.board)
        pygame.display.flip()
        before = self.game.board.copy()
        result = self.game.computer_move()          # blocks while searching
        self.board_view.animate_drop(
            self.screen, before, result.column, config.AI,
            lambda: self._draw_frame(before, hover=False),
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
        scores = self.font.render(f"You (red): {human}    Computer (yellow): {ai}", True, theme.TEXT)
        status = self.small.render(self.status, True, theme.TEXT_DIM)
        self.screen.blit(scores, (40, 30))
        self.screen.blit(status, (40, 70))

        hover_col = None
        if hover and self.state == "play" and self.game.current_player == config.HUMAN:
            hover_col = self.board_view.column_at(pygame.mouse.get_pos())
        self.board_view.draw(self.screen, board, hover_col)
        self.tree_view.draw(self.screen)

        if self.state == "over":
            winner = self.game.result().winner
            text = "You win!" if winner == config.HUMAN else "Computer wins" if winner == config.AI else "Draw"
            banner = self.big.render(text, True, theme.TEXT)
            hint = self.small.render("Press R for the menu", True, theme.TEXT)
            self.screen.blit(banner, (40, 660))
            self.screen.blit(hint, (300, 675))

    # ---- main loop -----------------------------------------------------
    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif self.state == "menu":
                    if self.menu.handle_event(event):
                        self.start_game(self.menu.selected_k(), self.menu.selected_heuristic())
                else:
                    self.tree_view.handle_event(event)
                    if event.type == pygame.KEYDOWN and event.key in (pygame.K_r, pygame.K_ESCAPE):
                        self.state = "menu"
                    elif (self.state == "play" and event.type == pygame.MOUSEBUTTONDOWN
                          and event.button == 1 and self.game.current_player == config.HUMAN):
                        self._human_click(event.pos)

            if (self.state == "play" and not self.game.is_over()
                    and self.game.current_player == config.AI):
                self._ai_turn()

            self._draw_frame(self.game.board if self.game else Board())
            pygame.display.flip()
            self.clock.tick(theme.FPS)
        pygame.quit()


def run_gui(k: int | None = None, heuristic_name: str | None = None,
            human_starts: bool = True, use_pruning: bool = True) -> None:
    """Open the window. If both k and heuristic_name are given, skip the menu."""
    _GuiApp(k, heuristic_name, human_starts, use_pruning).run()
