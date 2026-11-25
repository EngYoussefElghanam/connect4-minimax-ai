# Student A — Understand and defend all 47 functions

**Purpose:** A quick walkthrough of the files you own, the reasoning behind them, and the questions an instructor can ask. The code is in `src/connect4/`, `src/connect4/ai/`, and `benchmarks/`.

## 0. The entire program in one picture

```text
Console / GUI (your teammates)
       |
       v
Game.human_move / Game.computer_move
       |                    |
       |                    v
       |              MinimaxAgent.choose_move
       |                    |
       |                    v
       |              _search(board, depth, alpha, beta, maximizing)
       |                 /     |       \
       |           Board  Heuristic    TreeNode + SearchStats
       |          .with_move  .evaluate   (values/prunes/counters)
       |                 \     |       /
       |                    v
       |           chosen column + tree + statistics
       v
Board.drop_piece, scoring.get_scores, scoring.winner
```

**Core assignment peculiarity:** Forming a four-in-a-row is **not** a terminal condition. Play continues until all 42 spaces are occupied. Final winner is based on the **number of 4-cell windows** each player owns, rather than who reaches a four first.

## 1. Board fundamentals: `config.py` and `board.py` (17 functions)

A 6-row by 7-column grid is stored as a list of lists of integers. `0` means empty, `1` human, `2` computer. Row zero is **top**, row five is **bottom**. Columns 0..6 are internal; the human-facing UI should convert 1..7 to 0..6.

| Function | What it is responsible for |
|---|---|
| `__init__(rows, cols)` | Allocate distinct rows filled with zeroes. |
| `from_strings(rows)` | Convert `.`, `H`, `A` diagrams into a Board for tests. It deliberately doesn't check gravity in fixtures. |
| `to_strings()` | Reconstruct that same diagram. |
| `copy()` | Deep-copy the grid so modifying one search child doesn't change its parent. |
| `swapped()` | Exchange human/AI pieces in a new Board; useful when testing heuristic symmetry. |
| `rows`, `cols` | Read-only properties for grid dimensions. |
| `get(row, col)` | Read one cell. |
| `is_valid_move(col)` | Reject out-of-range columns and columns whose top cell is occupied. |
| `valid_moves()` | Enumerate legal columns in increasing order. |
| `is_full()` | True when no legal column remains. |
| `count_pieces(player)` | Count just one player's discs, or all nonempty cells. |
| `next_open_row(col)` | Find the **lowest** empty cell in a column (gravity). |
| `drop_piece(col, player)` | Mutate this board by placing one disc; return its landing row. |
| `with_move(col, player)` | Copy first, then drop on the copy; used for search children. |
| `__eq__(other)` | Compare the complete board contents and dimensions. |
| `__hash__()` | Hash an immutable snapshot of the current grid; **never mutate a Board while it's a dictionary key**. |

**Trace it:** On an empty 6x7 board, `drop_piece(3, AI)` writes to `grid[5][3]`; a second `drop_piece(3, HUMAN)` writes to `grid[4][3]`. `with_move(3, AI)` changes **only** the returned child, not the original Board.

## 2. Counting connected fours: `scoring.py` (5 functions)

We scan every possible 4-cell window in each of four directions:

- horizontal `(dr,dc) = (0,1)`
- vertical `(1,0)`
- downward-right `(1,1)`
- upward-right `(-1,1)`

We only include a window when its ending coordinate stays inside the grid. On a 6×7 board, there are **69 total**: 24 horizontal + 21 vertical + 12 down-diagonal + 12 up-diagonal.

| Function | Meaning |
|---|---|
| `iter_windows(board)` | Yield each unique 4-position coordinate window. |
| `count_connect_fours(board, player)` | Count windows where **all four cells** equal that player. |
| `get_scores(board)` | Return `(human_score, ai_score)` in that order. |
| `score_difference(board)` | Return `ai_score - human_score`. Positive means computer leads. |
| `winner(board)` | Larger final score wins; 0 difference means a tie. |

**Why overlaps count:** `AAAAA..` has two 4-cell windows: columns 0–3 and columns 1–4. Thus it scores **2**, not 1.

## 3. Difficulty and statistics (4 functions)

`difficulty.py`: `validate_k` accepts only a positive integer, `difficulty_from_name` converts text to an enum, and `k_for_difficulty` converts EASY/MEDIUM/HARD to their K depths (currently 2/4/6). There is no maximum K; searching or printing K=10 may be very slow.

`stats.py`: `SearchStats.reset()` zeroes `nodes_expanded`, `leaf_evaluations`, `prunes`, `elapsed_seconds`, and `max_depth_reached` so every computer turn has independent measurements.

## 4. Building the traceable tree: `tree.py` (3 functions)

`TreeNode` stores: `depth`, `is_max`, `move`, `board`, `value`, `children`, `pruned`, `is_leaf`, `alpha`, `beta`, and `heuristic_breakdown`. For a skipped branch, we save a **pruned placeholder** with `pruned=True` and `value=None`, since no heuristic was actually calculated for it.

- `iter_nodes(root)`: depth-first, **preorder** traversal — parent before children.
- `count_nodes(root, include_pruned=False)`: number actually searched, not invented placeholders.
- `tree_depth(root)`: greatest depth of any node; the root has depth zero.

Your teammate's console tree printer will read these objects. The minimax engine itself doesn't print anything.

## 5. Minimax and alpha-beta: `minimax.py` (5 functions)

**Why is the AI MAX?** Heuristics return positive values for good AI positions and negative values for good human positions. MAX chooses the highest score; MIN is a simulated rational human who chooses the lowest score.

Let `V(board, d)` be the position value at depth `d`. Conceptually:

```text
if board is full: V = final_score_ai - final_score_human
else if d == K: V = heuristic.evaluate(board)
else if MAX's turn: V = max(V(each AI child, d+1))
else if MIN's turn: V = min(V(each human child, d+1))
```

| Function | What to explain |
|---|---|
| `__init__` | Store heuristic, depth K, recording/pruning flags, and statistics. |
| `choose_move(board)` | Reset stats, build root, time recursive search, return column/value/tree/stats; never mutate input. |
| `_search(...)` | Visit node, stop at full/K, else recurse into children, alternate MAX/MIN, and prune when allowed. |
| `_evaluate_leaf(board)` | At full board use **exact final score difference**; at K use **heuristic**. |
| `_order_moves(board)` | Explore center columns first (3,2,4,1,5,0,6 on an empty 7-wide board). |

### Alpha-beta in one minute

- **Alpha** = best score MAX can already guarantee along this path (lower bound).
- **Beta** = best score MIN can already guarantee along this path (upper bound).
- At MAX: `best = max(best, child_value)`, then `alpha = max(alpha, best)`.
- At MIN: `best = min(best, child_value)`, then `beta = min(beta, best)`.
- When `alpha >= beta`, skip remaining siblings: this subtree cannot alter the choice of an ancestor.

**Discussion example:** MAX has found a move worth `5`, so alpha is `5`. At another candidate, the opponent (MIN) finds a response worth `3`; its beta becomes `3`. Since `3 <= 5`, MAX will never prefer that second candidate, regardless of MIN's other responses. So exploring those remaining responses would be unnecessary.

**Counts:** With all seven columns available, unpruned K=2 visits `1 + 7 + 7² = 57` nodes. Pruned placeholders are shown in the tree but **not counted as evaluated**. The heuristic breakdown is stored at every evaluated leaf so the UI can display actual values, which the assignment requires.

### Important implementation decisions

1. The root (`depth=0`) is always a MAX node because this function is only called on an **AI turn**.
2. Every child is generated with `board.with_move`; input board is untouched.
3. Equal-valued best moves choose whichever is evaluated **first**; center-first ordering decides the tie.
4. Alpha-beta can change *which equally optimal move* is chosen, but not the exact minimax root value.
5. Printing a giant K=6 or K=10 tree can be much slower than just selecting a move; your UI teammate should provide a practical output/export option without hiding the tree required by the assignment.

## 6. Controller: `game.py` (8 functions)

| Function | Meaning |
|---|---|
| `Game.__init__` | Validate K, create board and agent, choose starting player. |
| `board` | Expose current board. |
| `current_player` | Expose whose turn it is. |
| `is_over()` | Only true when the board is **full**. |
| `human_move(col)` | Reject wrong turn/illegal move, drop H, then hand turn to AI. |
| `computer_move()` | Run minimax, drop A in chosen column, return search result for UI. |
| `scores()` | Get running totals as `(human, ai)`. |
| `result()` | Only on full board, report both scores and winner. |

Example: `Game(k=2, heuristic=...)` starts with HUMAN. After `game.human_move(3)`, it is AI's turn. `game.computer_move()` calls minimax and returns a `SearchResult` that includes the tree and performance stats.

## 7. Benchmark: `benchmarks/k_analysis.py` (5 functions)

| Function | Meaning |
|---|---|
| `sample_positions()` | Reproducible empty/early/middle/late boards; same inputs for both algorithms. |
| `run_k_analysis()` | Vary K and pruning on/off, measure nodes/time and prune counts. |
| `write_csv()` | Write these real observed results, not estimates. |
| `plot_results()` | Create time-vs-K and nodes-vs-K charts with matplotlib. |
| `main()` | Parse CLI flags and invoke the experiment. |

Use `python benchmarks/k_analysis.py --kmin 1 --kmax 4 --heuristic composite --plot` **after your heuristic teammate completes their files**. Plain minimax is deliberately skipped at K>5 because it can be extremely expensive. Report averages over multiple positions and label your computer's hardware. Do not claim timings are universal.

## 8. Your teacher may ask these questions

**Q: Why can the game keep running after somebody gets 4 in a row?**
A: The assignment explicitly requires a full-board game; the score is total connected-fours, not classic first-four wins.

**Q: Why doesn't minimax explore to the end?**
A: The branching factor is up to 7, so the tree grows exponentially. We stop at depth K and estimate the board with a heuristic.

**Q: What is the difference between minimax and alpha-beta?**
A: They return the same optimal root **value** at a fixed depth and heuristic. Alpha-beta avoids visiting subtrees unable to change the best decision.

**Q: What does alpha >= beta tell you?**
A: A bound proves the remaining children cannot influence the result selected by an ancestor.

**Q: Does a pruned node have a heuristic score?**
A: No. It was never evaluated. The tree includes a placeholder to make the skipped branches visible.

**Q: Why copy the board?**
A: Each imagined move is an independent hypothetical game state. Without copies, one branch's pieces could leak into another branch.

**Q: Why center-first?**
A: Better ordering often discovers strong moves earlier, causing more cutoffs; it is not a correctness requirement.

**Q: Is K=4 four complete rounds?**
A: No. K is **four plies**, i.e., four individual moves, commonly two AI moves and two human replies.

**Q: What if K=1?**
A: Try every legal AI move, evaluate each resulting board immediately, choose the highest value.

**Q: What is terminal utility?**
A: On a full board, the actual objective is `AI_connected_fours - human_connected_fours` rather than an estimated heuristic.

**Q: Why can two computers give different timings?**
A: CPU, load, Python versions, tree recording, board position, and heuristics affect runtime. Use a consistent environment in comparisons.

**Q: What does 69 mean?**
A: There are 69 four-cell windows on a 6×7 board, covering horizontal, vertical, and both diagonal directions.

**Q: Why does `AAAAA` count as two?**
A: Two overlapping sets of four consecutive cells exist: 0–3 and 1–4.

## 9. Verification (before and after teammates merge)

From project root:

```bash
python -m pip install -r requirements.txt
python -m pytest -q tests/test_board.py tests/test_scoring.py tests/test_difficulty.py tests/test_student_a_isolated.py
```

The isolated tests use a tiny **test-only** score-difference heuristic because your teammate's production heuristic files are still TODOs. Once their heuristics are implemented, run:

```bash
python -m pytest -q tests/test_minimax.py tests/test_tree.py tests/test_alpha_beta_equivalence.py tests/test_game.py tests/test_benchmark.py
python -m pytest -q
python benchmarks/k_analysis.py --kmin 1 --kmax 4 --heuristic composite --plot
```

The **original skeleton contains a test-data mistake:** `tests/sample_boards.py` originally had `MID_GAME` with 9 pieces (5 H, 4 A), while tests expect 8 (4 H, 4 A). This package corrects the last row from `.AHHAH.` to `.AHHA..`, without altering the board-counting algorithm. You should mention the correction in your PR.

Finally, the console/GUI files and production heuristics are currently unimplemented. Running `python main.py` cannot work until those teammates' modules are finished. That does not mean Student A's search code is broken.
