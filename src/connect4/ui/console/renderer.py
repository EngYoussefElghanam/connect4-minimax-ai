"""Turn game objects into strings. No printing here."""
from __future__ import annotations

from connect4.board import Board


def render_board(board: Board) -> str:
    """Multi-line board drawing: top row first, then a footer with column numbers 1..cols.
    Use distinct symbols for HUMAN, AI and empty."""
    # TODO
    raise NotImplementedError


def render_scores(human_score: int, ai_score: int) -> str:
    """One-line scoreboard, e.g. 'You: 1 | Computer: 2'."""
    # TODO
    raise NotImplementedError


def render_stats(nodes_expanded: int, elapsed_seconds: float, prunes: int) -> str:
    """One-line search summary shown after each computer move."""
    # TODO
    raise NotImplementedError
