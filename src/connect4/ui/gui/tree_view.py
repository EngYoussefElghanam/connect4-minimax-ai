"""Interactive minimax-tree panel (GUI bonus): expand/collapse nodes, show values,
highlight the chosen path and pruned branches."""
from __future__ import annotations

from connect4.ai.tree import TreeNode


class TreeView:
    def __init__(self, screen) -> None:
        # TODO
        raise NotImplementedError

    def set_tree(self, root: TreeNode | None) -> None:
        # TODO: store tree, reset scroll/collapse state
        raise NotImplementedError

    def handle_event(self, event) -> None:
        """Click to expand/collapse, mouse wheel to scroll."""
        # TODO
        raise NotImplementedError

    def draw(self) -> None:
        # TODO
        raise NotImplementedError
