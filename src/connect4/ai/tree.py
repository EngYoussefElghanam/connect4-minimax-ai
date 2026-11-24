"""Captured search tree; the UI formats these TreeNode objects for display."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterator

from connect4.board import Board


@dataclass
class TreeNode:
    depth: int
    is_max: bool
    move: int | None
    board: Board | None = None
    value: float | None = None
    is_leaf: bool = False
    pruned: bool = False
    alpha: float | None = None
    beta: float | None = None
    heuristic_breakdown: dict[str, float] | None = None
    children: list["TreeNode"] = field(default_factory=list)


def iter_nodes(root: TreeNode) -> Iterator[TreeNode]:
    """Preorder DFS: parent, then its children from left to right."""
    yield root
    for child in root.children:
        yield from iter_nodes(child)


def count_nodes(root: TreeNode, include_pruned: bool = True) -> int:
    return sum(1 for n in iter_nodes(root) if include_pruned or not n.pruned)


def tree_depth(root: TreeNode) -> int:
    return max(node.depth for node in iter_nodes(root))
