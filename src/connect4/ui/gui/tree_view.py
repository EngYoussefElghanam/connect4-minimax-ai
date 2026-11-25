"""Scrollable, collapsible view of the last search tree."""
from __future__ import annotations

import pygame

from connect4 import config
from connect4.ai.tree import TreeNode
from connect4.ui.console.tree_printer import format_node
from connect4.ui.gui import theme


class TreeView:
    def __init__(self, rect, font: pygame.font.Font):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.heading = pygame.font.Font(None, 36)
        self.small = pygame.font.Font(None, 20)
        self.colours = {config.HUMAN: theme.HUMAN_COLOUR, config.AI: theme.AI_COLOUR}
        self.root: TreeNode | None = None
        self.expanded: set[int] = set()
        self.scroll = 0
        self.horizontal = 0

    def set_tree(self, root: TreeNode | None) -> None:
        self.root = root
        self.expanded = {id(root)} if root is not None else set()
        self.scroll = 0
        self.horizontal = 0

    # ---- helpers -------------------------------------------------------
    def _visible_rows(self) -> list[tuple[TreeNode, int]]:
        """Preorder list of (node, depth), descending only into expanded nodes."""
        if self.root is None:
            return []
        rows: list[tuple[TreeNode, int]] = []
        stack = [(self.root, 0)]
        while stack:
            node, depth = stack.pop()
            rows.append((node, depth))
            if id(node) in self.expanded:
                for child in reversed(node.children):
                    stack.append((child, depth + 1))
        return rows

    def _capacity(self) -> int:
        return (self.rect.height - theme.TREE_HEADER_HEIGHT) // theme.TREE_LINE_HEIGHT

    def _clamp_scroll(self, total: int) -> None:
        self.scroll = max(0, min(self.scroll, total - self._capacity()))

    # ---- events --------------------------------------------------------
    def handle_event(self, event: pygame.event.Event, pointer=None) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.horizontal = max(0, self.horizontal + (100 if event.key == pygame.K_RIGHT else -100))
        elif event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pointer if pointer is not None else pygame.mouse.get_pos()):
            self.scroll -= event.y * 3
            self._clamp_scroll(len(self._visible_rows()))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                and self.rect.collidepoint(event.pos):
            if event.pos[1] < self.rect.y + theme.TREE_HEADER_HEIGHT:
                return
            rows = self._visible_rows()
            index = (event.pos[1] - self.rect.y - theme.TREE_HEADER_HEIGHT) // theme.TREE_LINE_HEIGHT
            index += self.scroll
            if 0 <= index < len(rows):
                node = rows[index][0]
                if node.children:
                    key = id(node)
                    if key in self.expanded:
                        self.expanded.discard(key)
                    else:
                        self.expanded.add(key)

    # ---- drawing -------------------------------------------------------
    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, theme.PANEL, self.rect, border_radius=18)
        left, top = self.rect.left, self.rect.top
        surface.blit(self.heading.render("Search tree", True, theme.TEXT), (left + 20, top + 12))
        hint = "Click branches to expand   /   Scroll   /   Arrow keys to pan"
        surface.blit(self.small.render(hint, True, theme.TEXT_DIM), (left + 20, top + 45))
        rows = self._visible_rows()
        if not rows:
            words = self.small.render("The computer's first move will appear here.", True, theme.TEXT_DIM)
            surface.blit(words, words.get_rect(center=self.rect.center))
            return
        self._clamp_scroll(len(rows))
        previous = surface.get_clip()
        body = self.rect.inflate(-20, 0)
        body.top += theme.TREE_HEADER_HEIGHT
        body.height = self.rect.bottom - body.top - 5
        surface.set_clip(body)
        for i, (node, depth) in enumerate(rows[self.scroll:self.scroll + self._capacity()]):
            y = body.top + i * theme.TREE_LINE_HEIGHT
            x = body.left + 10 + depth * 18 - self.horizontal
            if depth:
                pygame.draw.lines(surface, theme.EDGE, False,
                                  [(x-10,y), (x-10,y+25), (x-2,y+25)], 2)
            if node.board is not None:
                for r in range(config.ROWS):
                    for c in range(config.COLS):
                        v = node.board.get(r, c)
                        pygame.draw.circle(surface, self.colours.get(v, theme.EDGE),
                                           (x+4+c*7, y+9+r*7), 3)
            marker = ("- " if id(node) in self.expanded else "+ ") if node.children else ""
            role = "MAX" if node.is_max else "MIN"
            move = "Root" if node.move is None else f"Column {node.move + 1}"
            title = self.small.render(f"{marker}{move}   /   {role}", True, theme.TEXT)
            surface.blit(title, (x+58, y+7))
            detail = format_node(node).split(" ", 2)[-1]
            surface.blit(self.font.render(detail, True, theme.TEXT_DIM), (x+58, y+28))
            pygame.draw.line(surface, theme.EDGE, (body.x, y+54), (body.right, y+54))
        surface.set_clip(previous)
