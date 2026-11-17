"""Global constants. Keep every tunable number here so the report can cite one place."""

# --- Board -----------------------------------------------------------------
ROWS = 6          # height (>= 6 required by the assignment)
COLS = 7          # width  (>= 7 required by the assignment)
CONNECT = 4       # discs needed for one "connected-four"

# --- Cell values -----------------------------------------------------------
EMPTY = 0
HUMAN = 1
AI = 2

# --- Search depth (K) --------------------------------------------------------
MIN_K = 1
MAX_K = 10        # TODO: decide an upper bound that keeps the UI responsive

# TODO: tune these after running benchmarks/k_analysis.py
DIFFICULTY_K = {
    "EASY": 2,
    "MEDIUM": 4,
    "HARD": 6,
}

# --- Heuristic weights (used by CompositeHeuristic) ------------------------
# TODO: tune after experiments; document the final values in the report.
HEURISTIC_WEIGHTS = {
    "score_diff": 100.0,
    "open_windows": 10.0,
    "positional": 1.0,
    "threats": 25.0,
}
