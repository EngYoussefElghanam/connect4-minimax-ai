"""UI-independent human vs AI controller. A game ends only on a full board."""
from __future__ import annotations

from dataclasses import dataclass

from connect4 import config
from connect4.board import Board
from connect4.scoring import get_scores, winner
from connect4.ai.difficulty import validate_k
from connect4.ai.heuristics.base import Heuristic
from connect4.ai.minimax import MinimaxAgent, SearchResult


@dataclass
class GameResult:
    human_score: int
    ai_score: int
    winner: int | None


class Game:
    def __init__(self, k: int, heuristic: Heuristic, board: Board | None = None,
                 human_starts: bool = True, use_pruning: bool = True) -> None:
        validate_k(k)
        self._board = board.copy() if board is not None else Board()
        self._current_player = config.HUMAN if human_starts else config.AI
        self._agent = MinimaxAgent(heuristic, k, use_pruning=use_pruning)

    @property
    def board(self) -> Board:
        return self._board

    @property
    def current_player(self) -> int:
        return self._current_player

    def is_over(self) -> bool:
        return self._board.is_full()

    def human_move(self, col: int) -> int:
        if self.is_over():
            raise ValueError("game is over")
        if self.current_player != config.HUMAN:
            raise ValueError("it is not the human's turn")
        row = self._board.drop_piece(col, config.HUMAN)
        self._current_player = config.AI
        return row

    def computer_move(self) -> SearchResult:
        if self.is_over():
            raise ValueError("game is over")
        if self.current_player != config.AI:
            raise ValueError("it is not the computer's turn")
        result = self._agent.choose_move(self._board)
        self._board.drop_piece(result.column, config.AI)
        self._current_player = config.HUMAN
        return result

    def scores(self) -> tuple[int, int]:
        return get_scores(self._board)

    def result(self) -> GameResult:
        if not self.is_over():
            raise ValueError("final result is only available when the board is full")
        human, ai = self.scores()
        return GameResult(human, ai, winner(self._board))
