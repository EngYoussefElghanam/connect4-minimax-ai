"""Printable minimax tree. The agent builds this while searching (when record_tree=True)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from connect4.board import Board


@dataclass
class TreeNode:
    depth: int                       # root = 0
    is_max: bool                     # True = computer's (MAX) node, False = human's (MIN) node
    move: int | None                 # column played to reach this node (None for the root)
    board: Board | None = None       # snapshot (needed for "show board values" + GUI)
    value: float | None = None       # backed-up minimax value (or heuristic value at a leaf)
    is_leaf: bool = False            # True when evaluated by heuristic/terminal test
    pruned: bool = False             # True when alpha-beta cut this node off (never evaluated)
    alpha: float | None = None       # alpha when the node finished (for tracing)
    beta: float | None = None        # beta when the node finished (for tracing)
    heuristic_breakdown: dict[str, float] | None = None  # per-factor values at leaves
    children: list["TreeNode"] = field(default_factory=list)


def iter_nodes(root: TreeNode) -> Iterator[TreeNode]:
    """Depth-first (pre-order) iteration over every node."""
    # TODO
    raise NotImplementedError


def count_nodes(root: TreeNode, include_pruned: bool = True) -> int:
    """Total nodes in the tree."""
    # TODO
    raise NotImplementedError


def tree_depth(root: TreeNode) -> int:
    """Deepest node depth (root alone = 0)."""
    # TODO
    raise NotImplementedError
