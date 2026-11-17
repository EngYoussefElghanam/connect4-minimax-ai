"""Heuristic interface.

Sign convention (tests enforce it):
  positive  -> computer (AI) is better
  negative  -> human is better
  0         -> equal / empty board
Heuristics must be symmetric: evaluate(b) == -evaluate(b.swapped()).
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from connect4.board import Board


class Heuristic(ABC):
    name: str = "base"

    @abstractmethod
    def evaluate(self, board: Board) -> float:
        """Single number for the whole board (see sign convention above). Must not mutate board."""

    @abstractmethod
    def breakdown(self, board: Board) -> dict[str, float]:
        """Per-factor contributions, already weighted, so that
        sum(breakdown(b).values()) == evaluate(b). The tree printer shows this
        at the leaves ("show the values of board after applying the heuristic")."""
