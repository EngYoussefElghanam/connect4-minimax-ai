"""Readable, traceable text form of the minimax tree (required by the assignment)."""
from __future__ import annotations

from pathlib import Path

from connect4.ai.tree import TreeNode
from connect4.ui.console.renderer import render_board

INDENT = "    "


def _num(x: float | None) -> str:
    return "None" if x is None else f"{x:g}"


def format_node(node: TreeNode) -> str:
    """One line per node, e.g. '[MAX] col=4 value=12.5' or '[MIN] col=5 PRUNED'."""
    role = "MAX" if node.is_max else "MIN"
    head = f"[{role}] " + ("root" if node.move is None else f"col={node.move + 1}")
    if node.pruned:
        return f"{head} PRUNED"
    text = f"{head} value={_num(node.value)}"
    if node.alpha is not None and node.beta is not None:
        text += f" alpha={_num(node.alpha)} beta={_num(node.beta)}"
    if node.is_leaf:
        text += " leaf"
        if node.heuristic_breakdown:
            detail = ", ".join(f"{k}: {v:g}" for k, v in node.heuristic_breakdown.items())
            text += f" {{{detail}}}"
    return text


def format_tree(root: TreeNode, max_depth: int | None = None,
                show_boards: bool = False) -> str:
    """Indented preorder dump, one line per node unless show_boards is True.

    max_depth truncates printing (root = 0). With show_boards, the board is
    drawn under each leaf.
    """
    lines: list[str] = []

    def walk(node: TreeNode) -> None:
        pad = INDENT * node.depth
        hidden = (max_depth is not None and node.depth >= max_depth and node.children)
        lines.append(pad + format_node(node)
                     + (f" ... ({len(node.children)} children hidden)" if hidden else ""))
        if show_boards and node.is_leaf and node.board is not None:
            lines.extend(pad + INDENT + row for row in render_board(node.board).splitlines())
        if hidden:
            return
        for child in node.children:
            walk(child)

    walk(root)
    return "\n".join(lines)


def write_tree_to_file(root: TreeNode, path: str | Path, **kwargs) -> Path:
    """Dump format_tree(root, **kwargs) to a text file, creating parent folders."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(format_tree(root, **kwargs) + "\n", encoding="utf-8")
    return target
