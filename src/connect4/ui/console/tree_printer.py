"""Readable, traceable text form of the minimax tree (REQUIRED by the assignment)."""
from __future__ import annotations

from connect4.ai.tree import TreeNode


def format_node(node: TreeNode) -> str:
    """One line for one node, e.g.
        '[MAX] col=4 value=12.5'                       (internal node)
        '[MIN] col=2 leaf heuristic=7.0 {score_diff: 0, open_windows: 7}'
        '[MIN] col=5 PRUNED'
    Must contain MAX/MIN, the column (1-based for humans), the value, and a PRUNED marker."""
    # TODO
    raise NotImplementedError


def format_tree(root: TreeNode, max_depth: int | None = None, show_boards: bool = False) -> str:
    """Indented tree, ONE LINE PER NODE when show_boards is False (tests rely on this).
    max_depth truncates printing (root = 0). With show_boards=True, print the board
    under each leaf together with its heuristic value."""
    # TODO
    raise NotImplementedError


def write_tree_to_file(root: TreeNode, path: str, **kwargs) -> None:
    """Dump format_tree(...) to a text file (for the report's sample runs)."""
    # TODO
    raise NotImplementedError
