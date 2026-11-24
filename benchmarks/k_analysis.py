"""Compare runtime and visited-node counts at several depth limits K.

    python benchmarks/k_analysis.py --kmin 1 --kmax 4 --out benchmarks/results/k_analysis.csv --plot
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from connect4 import config  # noqa: E402
from connect4.board import Board  # noqa: E402
from connect4.ai.difficulty import validate_k  # noqa: E402
from connect4.ai.heuristics import get_heuristic  # noqa: E402
from connect4.ai.minimax import MinimaxAgent  # noqa: E402

FIELDS = ["k", "heuristic", "pruning", "position_index", "nodes_expanded", "prunes", "time_seconds"]
# Without alpha-beta, 7^6 nodes can make a seemingly small test painfully slow.
MAX_PLAIN_K = 5


def sample_positions() -> list[Board]:
    """Fixed positions: empty, early, mid, and later; all are gravity-valid."""
    positions = [Board()]
    board = Board()
    for turn, col in enumerate([3, 2, 4, 3, 2, 4, 3, 2, 5, 1,
                                4, 5, 0, 6, 3, 4, 1, 5, 6, 0,
                                2, 5, 4, 6, 1, 0]):
        board.drop_piece(col, config.HUMAN if turn % 2 == 0 else config.AI)
        if turn in (3, 11, 25):
            positions.append(board.copy())
    return positions


def run_k_analysis(k_values: list[int], heuristic_name: str,
                   positions: list[Board] | None = None,
                   include_no_pruning: bool = True) -> list[dict]:
    positions = sample_positions() if positions is None else positions
    heuristic = get_heuristic(heuristic_name)
    rows = []
    for k in k_values:
        validate_k(k)
        for pruning in ([True, False] if include_no_pruning else [True]):
            if not pruning and k > MAX_PLAIN_K:
                continue  # documented safety cap; do not fabricate measurements
            for i, board in enumerate(positions):
                if board.is_full():
                    continue
                agent = MinimaxAgent(heuristic, k, use_pruning=pruning,
                                     record_tree=False, record_boards=False)
                result = agent.choose_move(board)
                rows.append({
                    "k": k,
                    "heuristic": heuristic_name,
                    "pruning": pruning,
                    "position_index": i,
                    "nodes_expanded": result.stats.nodes_expanded,
                    "prunes": result.stats.prunes,
                    "time_seconds": result.stats.elapsed_seconds,
                })
    return rows


def write_csv(rows: list[dict], path: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def plot_results(csv_path: str, out_dir: str) -> None:
    import matplotlib.pyplot as plt

    with open(csv_path, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    if not rows:
        raise ValueError("CSV contains no benchmark rows")
    dest = Path(out_dir)
    dest.mkdir(parents=True, exist_ok=True)
    for field, filename, ylabel in [
        ("time_seconds", "time_vs_k.png", "Mean elapsed time (seconds)"),
        ("nodes_expanded", "nodes_vs_k.png", "Mean nodes expanded"),
    ]:
        groups = defaultdict(list)
        for row in rows:
            groups[(row["pruning"].lower() == "true", int(row["k"]))].append(float(row[field]))
        fig, ax = plt.subplots(figsize=(8, 5))
        for pruning, label in [(True, "Alpha-beta"), (False, "Plain minimax")]:
            ks = sorted(k for p, k in groups if p == pruning)
            if ks:
                ax.plot(ks, [mean(groups[(pruning, k)]) for k in ks], marker="o", label=label)
        ax.set_xlabel("Depth limit K")
        ax.set_ylabel(ylabel)
        ax.set_title(f"{ylabel} vs K")
        ax.grid(alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(str(dest / filename), dpi=160)
        plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kmin", type=int, default=1)
    parser.add_argument("--kmax", type=int, default=4)
    parser.add_argument("--heuristic", default="score_diff")
    parser.add_argument("--out", default="benchmarks/results/k_analysis.csv")
    parser.add_argument("--plot", action="store_true")
    args = parser.parse_args()
    if args.kmax < args.kmin:
        parser.error("--kmax must be >= --kmin")
    rows = run_k_analysis(list(range(args.kmin, args.kmax + 1)), args.heuristic)
    write_csv(rows, args.out)
    print(f"Saved {len(rows)} benchmark measurements to {args.out}")
    if args.kmax > MAX_PLAIN_K:
        print(f"Plain minimax intentionally skipped for K > {MAX_PLAIN_K}")
    if args.plot:
        plot_results(args.out, str(Path(args.out).parent))
        print("Saved time_vs_k.png and nodes_vs_k.png")


if __name__ == "__main__":
    main()
