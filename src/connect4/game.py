"""Game controller: owns the board, whose turn it is, and the AI agent.
No printing and no input() in here — UIs call these methods."""
from __future__ import annotations

from dataclasses import dataclass

from connect4.board import Board
from connect4.ai.heuristics.base import Heuristic
from connect4.ai.minimax import MinimaxAgent, SearchResult


@dataclass
class GameResult:
    human_score: int
    ai_score: int
    winner: int | None   # HUMAN, AI, or None for a tie


class Game:
    def __init__(self, k: int, heuristic: Heuristic, board: Board | None = None,
                 human_starts: bool = True, use_pruning: bool = True) -> None:
        """Validate k (ai.difficulty.validate_k), build the MinimaxAgent, set first player."""
        # TODO
        raise NotImplementedError

    @property
    def board(self) -> Board:
        # TODO
        raise NotImplementedError

    @property
    def current_player(self) -> int:
        # TODO
        raise NotImplementedError

    def is_over(self) -> bool:
        """Game ends only when the board is full."""
        # TODO
        raise NotImplementedError

    def human_move(self, col: int) -> int:
        """Apply the human's move. Returns landing row. Raises ValueError if illegal
        or if it is not the human's turn."""
        # TODO
        raise NotImplementedError

    def computer_move(self) -> SearchResult:
        """Run minimax, apply the chosen column, return the full SearchResult
        (column, value, tree, stats) so the UI can print the tree."""
        # TODO
        raise NotImplementedError

    def scores(self) -> tuple[int, int]:
        """(human_score, ai_score) right now."""
        # TODO
        raise NotImplementedError

    def result(self) -> GameResult:
        """Final result. Raises ValueError if the game is not over."""
        # TODO
        raise NotImplementedError
