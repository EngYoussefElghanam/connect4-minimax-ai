"""Resettable counters for the report's time/depth/K comparison."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchStats:
    nodes_expanded: int = 0
    leaf_evaluations: int = 0
    prunes: int = 0
    elapsed_seconds: float = 0.0
    max_depth_reached: int = 0

    def reset(self) -> None:
        self.nodes_expanded = 0
        self.leaf_evaluations = 0
        self.prunes = 0
        self.elapsed_seconds = 0.0
        self.max_depth_reached = 0
