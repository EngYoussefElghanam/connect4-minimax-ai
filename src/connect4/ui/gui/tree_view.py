"""Scrollable, collapsible view of the last search tree."""
from __future__ import annotations

import pygame

from connect4.ai.tree import TreeNode
from connect4.ui.console.tree_printer import format_node
from connect4.ui.gui import theme


class TreeView:
    def __init__(self, rect, font: pygame.font.Font):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.root: TreeNode | None = None
        self.expanded: set[int] = set()
        self.scroll = 0

    def set_tree(self, root: TreeNode | None) -> None:
        self.root = root
        self.expanded = {id(root)} if root is not None else set()
        self.scroll = 0

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
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.scroll -= event.y * 3
            self._clamp_scroll(len(self._visible_rows()))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                and self.rect.collidepoint(event.pos):
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
        pygame.draw.rect(surface, theme.PANEL, self.rect, border_radius=8)
        title = self.font.render("Search tree (click to expand, wheel to scroll)", True, theme.TEXT)
        surface.blit(title, (self.rect.x + 10, self.rect.y + 8))
        rows = self._visible_rows()
        if not rows:
            hint = self.font.render("Nothing yet: the tree appears after the computer moves.",
                                    True, theme.TEXT_DIM)
            surface.blit(hint, (self.rect.x + 10, self.rect.y + theme.TREE_HEADER_HEIGHT + 4))
            return
        self._clamp_scroll(len(rows))
        previous_clip = surface.get_clip()
        surface.set_clip(self.rect)
        y = self.rect.y + theme.TREE_HEADER_HEIGHT
        for node, depth in rows[self.scroll:self.scroll + self._capacity()]:
            marker = "  " if not node.children else ("- " if id(node) in self.expanded else "+ ")
            if node.pruned:
                colour = theme.PRUNED_COLOUR
            else:
                colour = theme.MAX_COLOUR if node.is_max else theme.MIN_COLOUR
            text = self.font.render("  " * depth + marker + format_node(node), True, colour)
            surface.blit(text, (self.rect.x + 10, y))
            y += theme.TREE_LINE_HEIGHT
        surface.set_clip(previous_clip)
