"""K-analysis for the report: time and nodes expanded vs K, with and without pruning.

    python benchmarks/k_analysis.py --kmin 1 --kmax 7 --out benchmarks/results/k_analysis.csv
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from connect4.board import Board  # noqa: E402


def sample_positions() -> list[Board]:
    """A few fixed positions (empty, early, mid, late game) so runs are comparable."""
    # TODO
    raise NotImplementedError


def run_k_analysis(k_values: list[int], heuristic_name: str,
                   positions: list[Board] | None = None,
                   include_no_pruning: bool = True) -> list[dict]:
    """For each K (and for pruning on/off): run MinimaxAgent on each position and
    return rows with EXACTLY these keys:
        k, heuristic, pruning (bool), position_index, nodes_expanded, prunes, time_seconds
    Guard plain-minimax runs against absurdly large K (skip or cap) so the script finishes."""
    # TODO
    raise NotImplementedError


def write_csv(rows: list[dict], path: str) -> None:
    # TODO
    raise NotImplementedError


def plot_results(csv_path: str, out_dir: str) -> None:
    """Make 'time vs K' and 'nodes vs K' charts (pruning vs no pruning) for the report."""
    # TODO (matplotlib)
    raise NotImplementedError


def main() -> None:
    """argparse: --kmin --kmax --heuristic --out --plot"""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    main()
