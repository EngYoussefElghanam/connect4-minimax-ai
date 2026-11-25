# Connect 4 — Minimax + Alpha-Beta AI Agent

Alexandria University · Faculty of Engineering · AI Course · Assignment 2 (due 25 Nov 2026)

## Layout

```
connect4-minimax/
├── main.py                     # entry point (CLI args -> console or GUI)
├── pytest.ini / requirements.txt
├── src/connect4/
│   ├── config.py               # constants: board size, players, minimum K, difficulty->K map
│   ├── board.py                # Board: grid, gravity drops, copy, helpers
│   ├── scoring.py              # count connected-fours, winner by greater count
│   ├── game.py                 # Game controller: turns, game over, result
│   ├── ai/
│   │   ├── minimax.py          # MinimaxAgent: minimax + alpha-beta, depth-limited by K
│   │   ├── tree.py             # TreeNode + tree utilities (the printable minimax tree)
│   │   ├── stats.py            # SearchStats: nodes expanded, pruned, time
│   │   ├── difficulty.py       # Difficulty enum, K validation, difficulty -> K
│   │   └── heuristics/         # one file per heuristic + registry (bonus: best 3)
│   └── ui/
│       ├── console/            # input parsing, board renderer, tree printer, CLI loop
│       └── gui/                # GUI bonus: board view, tree view, menu view
├── tests/                      # pytest suite (written first, fails until implemented)
├── benchmarks/                 # K-analysis script (time + nodes, with/without pruning)
├── report/                     # report template + sample runs
└── docs/design_decisions.md    # assumptions to settle BEFORE coding
```

## Run

```bash
pip install -r requirements.txt
pytest                # run the automated tests
python main.py        # console
python main.py --gui  # GUI
```

## Suggested implementation order (each step turns a test file green)

1. `board.py`        -> `tests/test_board.py`
2. `scoring.py`      -> `tests/test_scoring.py`
3. `ai/difficulty.py`-> `tests/test_difficulty.py`
4. `ai/tree.py`, `ai/stats.py`
5. `ai/heuristics/*` -> `tests/test_heuristics.py`
6. `ai/minimax.py`   -> `tests/test_minimax.py`, `tests/test_alpha_beta_equivalence.py`, `tests/test_tree.py`
7. `game.py`         -> `tests/test_game.py`
8. `ui/console/*`    -> `tests/test_input_parsing.py`, `tests/test_console_render.py`
9. `benchmarks/`     -> `tests/test_benchmark.py`
10. `ui/gui/*`       -> `tests/test_gui_smoke.py`

## GUI controls

Click the K field and type any positive integer (no maximum). Choose a heuristic and disc colour, then Start. Every AI turn prints the full explored tree and evaluated leaf boards to the terminal. Click tree nodes to expand, scroll vertically, or use Left/Right to pan. Large K can take impractically long and use substantial memory; start with K=1–4.
