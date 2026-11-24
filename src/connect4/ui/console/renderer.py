"""Turn game objects into strings. No printing here."""
from __future__ import annotations

from connect4 import config
from connect4.board import Board

SYMBOLS = {config.EMPTY: ".", config.HUMAN: "X", config.AI: "O"}


def render_board(board: Board) -> str:
    """Top row first, then a footer with the column numbers 1..cols."""
    lines = [" ".join(SYMBOLS[board.get(r, c)] for c in range(board.cols))
             for r in range(board.rows)]
    lines.append(" ".join(str(c + 1) for c in range(board.cols)))
    return "\n".join(lines)


def render_scores(human_score: int, ai_score: int) -> str:
    return f"You (X): {human_score} | Computer (O): {ai_score}"


def render_stats(nodes_expanded: int, elapsed_seconds: float, prunes: int) -> str:
    return (f"nodes expanded: {nodes_expanded} | prunes: {prunes} | "
            f"time: {elapsed_seconds:.3f}s")
