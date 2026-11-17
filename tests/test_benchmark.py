import csv

from connect4.board import Board
from benchmarks.k_analysis import run_k_analysis, sample_positions, write_csv

KEYS = {"k", "heuristic", "pruning", "position_index", "nodes_expanded", "prunes", "time_seconds"}


def test_sample_positions_are_boards():
    ps = sample_positions()
    assert ps and all(isinstance(p, Board) for p in ps)


def test_rows_have_expected_shape():
    rows = run_k_analysis([1, 2], "score_diff", positions=[Board()], include_no_pruning=True)
    assert len(rows) == 2 * 2 * 1          # K values x (pruning on/off) x positions
    assert all(set(r) == KEYS for r in rows)
    assert all(r["time_seconds"] >= 0 for r in rows)


def test_pruning_never_expands_more_nodes():
    rows = run_k_analysis([1, 2, 3], "score_diff", positions=[Board()], include_no_pruning=True)
    by = {(r["k"], r["pruning"]): r["nodes_expanded"] for r in rows}
    for k in (1, 2, 3):
        assert by[(k, True)] <= by[(k, False)]


def test_without_no_pruning_rows():
    rows = run_k_analysis([1], "score_diff", positions=[Board()], include_no_pruning=False)
    assert len(rows) == 1 and rows[0]["pruning"] is True


def test_write_csv_roundtrip(tmp_path):
    rows = run_k_analysis([1], "score_diff", positions=[Board()], include_no_pruning=False)
    out = tmp_path / "k.csv"
    write_csv(rows, str(out))
    with open(out, newline="") as f:
        read = list(csv.DictReader(f))
    assert len(read) == len(rows) and set(read[0]) == KEYS
