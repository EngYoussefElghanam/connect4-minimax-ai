"""Heuristic registry: lets the CLI/GUI list and pick heuristics by name."""
from __future__ import annotations

from connect4.ai.heuristics.base import Heuristic
from connect4.ai.heuristics.score_diff import ScoreDifferenceHeuristic
from connect4.ai.heuristics.open_windows import OpenWindowsHeuristic
from connect4.ai.heuristics.positional import PositionalHeuristic
from connect4.ai.heuristics.threats import ThreatHeuristic
from connect4.ai.heuristics.composite import CompositeHeuristic

ALL_HEURISTICS: dict[str, type[Heuristic]] = {
    "score_diff": ScoreDifferenceHeuristic,
    "open_windows": OpenWindowsHeuristic,
    "positional": PositionalHeuristic,
    "threats": ThreatHeuristic,
    "composite": CompositeHeuristic,
}


def get_heuristic(name: str) -> Heuristic:
    """Instantiate a heuristic by registry name. Raises ValueError for unknown names."""
    # TODO
    raise NotImplementedError
