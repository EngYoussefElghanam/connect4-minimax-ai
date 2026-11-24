"""Every completed four-cell window scores one point (overlaps count)."""
from __future__ import annotations

from collections.abc import Iterator

from connect4 import config
from connect4.board import Board


def iter_windows(board: Board) -> Iterator[list[tuple[int, int]]]:
    """All length-CONNECT windows in horizontal, vertical and both diagonals."""
    directions = ((0, 1), (1, 0), (1, 1), (-1, 1))
    for row in range(board.rows):
        for col in range(board.cols):
            for dr, dc in directions:
                end_r = row + (config.CONNECT - 1) * dr
                end_c = col + (config.CONNECT - 1) * dc
                if 0 <= end_r < board.rows and 0 <= end_c < board.cols:
                    yield [(row + i * dr, col + i * dc)
                           for i in range(config.CONNECT)]


def count_connect_fours(board: Board, player: int) -> int:
    if player not in (config.HUMAN, config.AI):
        raise ValueError("player must be HUMAN or AI")
    return sum(all(board.get(r, c) == player for r, c in window)
               for window in iter_windows(board))


def get_scores(board: Board) -> tuple[int, int]:
    return (count_connect_fours(board, config.HUMAN),
            count_connect_fours(board, config.AI))


def score_difference(board: Board) -> int:
    human, ai = get_scores(board)
    return ai - human


def winner(board: Board) -> int | None:
    diff = score_difference(board)
    return config.AI if diff > 0 else config.HUMAN if diff < 0 else None
