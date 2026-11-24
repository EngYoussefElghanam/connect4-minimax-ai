# Student A — Handoff and git commands

## What is finished

Student A's implementation: `board.py`, `scoring.py`, `ai/difficulty.py`,
`ai/stats.py`, `ai/tree.py`, `ai/minimax.py`, `game.py`, and
`benchmarks/k_analysis.py`. `config.py` already contains the required constants;
its existing values were intentionally retained.

Supporting deliverables: independent tests in `tests/test_student_a_isolated.py`,
this handoff, detailed explanation in `docs/STUDENT_A_LEARN_AND_DEFEND.md`,
report sections in `report/student_a_sections.md`, and pilot benchmark results.

## Teammate interface contracts

- **Heuristics teammate:** keep `Heuristic.evaluate(board) -> float` and
  `Heuristic.breakdown(board) -> dict[str,float]`. A leaf's breakdown should sum
  to its evaluated value. Implement `get_heuristic(name)` for the benchmark.
- **Console teammate:** `Game.computer_move()` returns `SearchResult(column,
  value, tree, stats)`. Print `tree` each AI turn; at leaves print
  `node.heuristic_breakdown` and optionally the stored board snapshot. A
  `node.pruned` branch has **no** value or evaluated board.
- **Main/GUI teammate:** create `Game(k=..., heuristic=..., human_starts=...)`;
  use `Game.board`, `Game.current_player`, `Game.human_move(0_based_column)`,
  `Game.computer_move()`, `Game.scores()`, `Game.is_over()`, `Game.result()`.

## The source-test inconsistency that was fixed

`tests/sample_boards.py`: The original `MID_GAME` fixture had 9 discs but
`test_board.py` expects 8 and 4 discs/player. Its bottom row was corrected from
`.AHHAH.` to `.AHHA..`. This was a fixture correction, **not** a change to
`Board.count_pieces()`; the latter correctly counted 9 on the original diagram.

## Safe merge (do not overwrite your teammates' live work)

The separate `student_A_changes.zip` contains only Student A's changed files
plus the one corrected fixture, isolated tests and supporting documentation.
Unzip it over your existing repo, preferably after creating a branch:

```bash
git switch -c student-a-engine-search
# Unzip student_A_changes.zip into the repository root using Finder or unzip.
python -m pip install -r requirements.txt
python -m pytest -q tests/test_board.py tests/test_scoring.py tests/test_difficulty.py tests/test_student_a_isolated.py
git add src/connect4/board.py src/connect4/scoring.py src/connect4/ai/difficulty.py \
        src/connect4/ai/stats.py src/connect4/ai/tree.py src/connect4/ai/minimax.py \
        src/connect4/game.py benchmarks/k_analysis.py tests/sample_boards.py \
        tests/test_student_a_isolated.py docs/STUDENT_A_LEARN_AND_DEFEND.md \
        docs/STUDENT_A_HANDOFF.md report/student_a_sections.md
git commit -m "Implement Connect 4 board, scoring, minimax alpha-beta, game engine and K benchmarks"
git push -u origin student-a-engine-search
```

Benchmark files are normally ignored by `.gitignore`. If your instructor or
team wants them in Git, force-add them explicitly:

```bash
git add -f benchmarks/results/student_a_baseline_k_analysis.csv \
           benchmarks/results/nodes_vs_k.png benchmarks/results/time_vs_k.png
```

## Validation

53 targeted tests passed on the package's Python 3.13 interpreter and another
45 randomly generated positions passed the consistency checks for alpha-beta
vs plain minimax (same value; pruning never expanded more nodes). The team's
full suite requires the other students to complete their heuristic, UI and
main.py skeleton files.

Additional check: 128 existing engine/search/game/benchmark tests passed in a
**temporary in-memory test process** that supplied minimal implementations of
the teammate heuristic interfaces. That process did not modify production
heuristic files and does not replace the full integrated test run after merge.
