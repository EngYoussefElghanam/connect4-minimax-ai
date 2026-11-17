"""Search statistics — feeds the K-analysis section of the report."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchStats:
    nodes_expanded: int = 0     # every node visited (internal + leaf)
    leaf_evaluations: int = 0   # heuristic / terminal evaluations
    prunes: int = 0             # number of alpha-beta cutoffs
    elapsed_seconds: float = 0.0
    max_depth_reached: int = 0

    def reset(self) -> None:
        # TODO
        raise NotImplementedError
