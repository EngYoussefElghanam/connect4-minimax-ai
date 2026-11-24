"""K-ply minimax with optional alpha-beta pruning and a traceable search tree.

AI maximizes evaluation, HUMAN minimizes it. A full board is the *only*
terminal position, so a four-in-a-row does not stop search prematurely.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import inf
from time import perf_counter

from connect4 import config
from connect4.board import Board
from connect4.scoring import score_difference
from connect4.ai.difficulty import validate_k
from connect4.ai.heuristics.base import Heuristic
from connect4.ai.stats import SearchStats
from connect4.ai.tree import TreeNode


@dataclass
class SearchResult:
    column: int
    value: float
    tree: TreeNode | None
    stats: SearchStats


class MinimaxAgent:
    def __init__(self, heuristic: Heuristic, k: int, use_pruning: bool = True,
                 record_tree: bool = True, record_boards: bool = True) -> None:
        self.k = validate_k(k)
        self.heuristic = heuristic
        self.use_pruning = use_pruning
        self.record_tree = record_tree
        self.record_boards = record_boards
        self.stats = SearchStats()
        self._best_root_move: int | None = None

    def choose_move(self, board: Board) -> SearchResult:
        if board.is_full():
            raise ValueError("cannot search moves on a full board")
        self.stats.reset()
        self._best_root_move = None
        root = TreeNode(depth=0, is_max=True, move=None,
                        board=board.copy() if self.record_boards else None) if self.record_tree else None
        start = perf_counter()
        value = self._search(board, 0, -inf, inf, True, root)
        self.stats.elapsed_seconds = perf_counter() - start
        assert self._best_root_move is not None
        # Snapshot statistics so a later choose_move() cannot change old results.
        stats_snapshot = SearchStats(**vars(self.stats))
        return SearchResult(self._best_root_move, value, root, stats_snapshot)

    def _search(self, board: Board, depth: int, alpha: float, beta: float,
                maximizing: bool, node: TreeNode | None) -> float:
        self.stats.nodes_expanded += 1
        self.stats.max_depth_reached = max(self.stats.max_depth_reached, depth)

        if depth == self.k or board.is_full():
            self.stats.leaf_evaluations += 1
            value = self._evaluate_leaf(board)
            if node is not None:
                node.is_leaf = True
                node.value = value
                node.alpha = alpha
                node.beta = beta
                node.heuristic_breakdown = (
                    {"terminal_score_diff": value} if board.is_full()
                    else self.heuristic.breakdown(board)
                )
            return value

        moves = self._order_moves(board)
        best = -inf if maximizing else inf
        player = config.AI if maximizing else config.HUMAN

        for index, col in enumerate(moves):
            child_board = board.with_move(col, player)
            child_node = None
            if node is not None:
                child_node = TreeNode(depth=depth + 1, is_max=not maximizing,
                                      move=col,
                                      board=child_board.copy() if self.record_boards else None)
                node.children.append(child_node)
            value = self._search(child_board, depth + 1, alpha, beta,
                                 not maximizing, child_node)
            if (maximizing and value > best) or (not maximizing and value < best):
                best = value
                if depth == 0:
                    self._best_root_move = col

            if self.use_pruning:
                if maximizing:
                    alpha = max(alpha, best)
                else:
                    beta = min(beta, best)
                if alpha >= beta:
                    # Record skipped siblings for tree printing, but do not
                    # count these placeholders as expanded/evaluated nodes.
                    skipped = moves[index + 1:]
                    if skipped:
                        self.stats.prunes += 1
                        if node is not None:
                            for skipped_col in skipped:
                                node.children.append(TreeNode(
                                    depth=depth + 1, is_max=not maximizing,
                                    move=skipped_col, pruned=True))
                    break

        if node is not None:
            node.value = best
            node.alpha = alpha
            node.beta = beta
        return best

    def _evaluate_leaf(self, board: Board) -> float:
        if board.is_full():
            # Final utility is explicitly the *number* of AI fours minus human fours.
            return float(score_difference(board))
        return float(self.heuristic.evaluate(board))

    def _order_moves(self, board: Board) -> list[int]:
        """Center-first ordering tends to produce earlier alpha-beta cutoffs."""
        middle = (board.cols - 1) / 2
        return sorted(board.valid_moves(), key=lambda c: (abs(c - middle), c))
