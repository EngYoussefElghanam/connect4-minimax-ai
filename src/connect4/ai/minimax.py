"""Minimax with alpha-beta pruning, truncated after K plies.

Conventions:
  * The computer (AI) is the MAX player, the human is the MIN player.
  * Depth counts plies from the root; stop when depth == k, the board is full,
    or no valid moves remain.
  * At a cut-off leaf: value = heuristic.evaluate(board).
    At a full board: value = terminal utility (final score difference).
  * use_pruning=False runs plain minimax (needed to compare nodes expanded in the report;
    both modes MUST return the same root value).
"""
from __future__ import annotations

from dataclasses import dataclass

from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic
from connect4.ai.stats import SearchStats
from connect4.ai.tree import TreeNode


@dataclass
class SearchResult:
    column: int                  # chosen column (0-based)
    value: float                 # minimax value of the root
    tree: TreeNode | None        # None when record_tree=False
    stats: SearchStats


class MinimaxAgent:
    def __init__(self, heuristic: Heuristic, k: int, use_pruning: bool = True,
                 record_tree: bool = True, record_boards: bool = True) -> None:
        """Validate k (raise ValueError if invalid) and store settings."""
        # TODO
        raise NotImplementedError

    def choose_move(self, board: Board) -> SearchResult:
        """Entry point. Must NOT mutate `board`. Raises ValueError if the board is full."""
        # TODO: reset stats, start timer, call the recursive search, stop timer
        raise NotImplementedError

    def _search(self, board: Board, depth: int, alpha: float, beta: float,
                maximizing: bool, node: TreeNode | None) -> float:
        """Recursive minimax / alpha-beta. Fills `node` (if recording) and updates stats."""
        # TODO: terminal / depth-limit test -> evaluate leaf
        # TODO: generate children (decide move ordering), recurse, update alpha/beta
        # TODO: on cutoff mark remaining children as pruned and increment stats.prunes
        raise NotImplementedError

    def _evaluate_leaf(self, board: Board) -> float:
        """Heuristic value for a cut-off node, or terminal utility for a full board."""
        # TODO
        raise NotImplementedError

    def _order_moves(self, board: Board) -> list[int]:
        """Order in which columns are explored (centre-first is a classic speed-up)."""
        # TODO
        raise NotImplementedError
