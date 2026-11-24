# Student A's report sections (draft for merging into the team report)

The implementation below is in `src/connect4/{board,scoring,game}.py`,
`src/connect4/ai/{minimax,difficulty,stats,tree}.py`, and
`benchmarks/k_analysis.py`. This text supplies sections 2, 3, 6 and 7 of the
team report and should be combined with the heuristic and interface sections.

## 2. Data structures

- **Board:** a 6-row × 7-column list-of-lists of integers, with 0=empty,
  1=human and 2=computer. Row 0 is the top of the board, so a newly dropped disc
  goes into the lowest empty row. Each imagined move in search uses a deep copy
  and leaves its parent position unchanged.
- **TreeNode:** a rooted tree capturing `depth`, move, MAX/MIN ownership,
  position snapshot, backed-up minimax value, alpha/beta bounds, children,
  leaf/pruned flags, and per-component heuristic values at evaluated leaves.
- **SearchStats:** counts visited nodes, evaluated leaves, cutoffs, deepest
  level and elapsed wall-clock time for each AI move. Counters are reset before
  every search.
- **Game:** holds the current board, player-to-move and minimax agent; it
  mediates legal moves between the frontend and the search algorithm.

## 3. Algorithms

### 3.1 Minimax and alpha-beta pruning

The computer is MAX, because all evaluation functions use positive numbers for
computer-favorable positions and negative numbers for human-favorable ones.
At each computer turn, the current board is the root of a K-ply search tree.
MAX nodes generate all legal AI drops and choose the maximum child value;
MIN nodes generate human drops and choose the minimum child value. Each child
is a new board with one legal move applied.

The search carries bounds alpha (best lower bound MAX can guarantee) and beta
(best upper bound MIN can guarantee). After each child, MAX updates alpha and
MIN updates beta. When `alpha >= beta`, the remaining siblings are not explored,
because they cannot change the best choice at an ancestor. Skipped siblings are
marked as pruned placeholders in the recorded tree, with no invented score.

Pseudocode:

```text
search(board, depth, alpha, beta, maximizing):
    if board_is_full(board): return score_ai(board) - score_human(board)
    if depth == K:          return heuristic(board)

    best = -infinity if maximizing else +infinity
    for column in legal_columns_center_first(board):
        child = board.with_move(column, AI if maximizing else HUMAN)
        value = search(child, depth+1, alpha, beta, not maximizing)
        best = max(best,value) if maximizing else min(best,value)
        if using_pruning:
            if maximizing: alpha = max(alpha,best)
            else:          beta = min(beta,best)
            if alpha >= beta: mark_skipped_siblings(); break
    return best
```

Exploring the middle columns first (3,2,4,1,5,0,6, zero-based) improves
pruning opportunities without changing the exact minimax value. Ties are
resolved in favor of the first explored optimal column. At depth K, leaf
values and their heuristic breakdowns are recorded for the console/GUI tree
printer. If the board becomes full before reaching K, its true final score
is used instead of the heuristic.

### 3.2 K-level truncation

K is the number of **individual moves (plies)** searched, not the number of
complete rounds. The unrestricted game tree grows exponentially; a full 7-way
unpruned tree to K=2 already contains 1+7+49=57 visited nodes on an empty board.
Therefore the leaf positions at depth K are estimated using a heuristic.
Only a completely full board is terminal: unlike ordinary Connect Four, making
a four does not end this assignment's game.

### 3.3 Difficulty parameter

The program accepts a custom K or one of three configured levels:
Easy K=2, Medium K=4, Hard K=6. Validation currently permits integer K in
1..10, but large K can become computationally impractical and tree-printing
can produce enormous output. The depth choice can be adjusted after runtime
measurements.

## 6. Time and nodes expanded versus K

**Method.** A preliminary real benchmark used four fixed, gravity-valid
positions (empty, after 4 moves, after 12 moves and after 26 moves). For each
position and K from 1 to 4, the same test-only score-difference heuristic was
used with and without alpha-beta pruning. Tree recording was disabled for a
fairer measurement of search work. Node counts include the root, every
internal node visited and every evaluated leaf; placeholders are excluded.

**Preliminary results** (means across the four positions; timings measured
in the supplied execution environment, not necessarily the team's hardware):

| K | Avg nodes, plain minimax | Avg nodes, alpha-beta | Avg seconds, plain | Avg seconds, alpha-beta |
|---|---:|---:|---:|---:|
| 1 | 8.0 | 8.0 | 0.0013 | 0.0010 |
| 2 | 56.8 | 35.0 | 0.0057 | 0.0033 |
| 3 | 394.2 | 118.0 | 0.0430 | 0.0118 |
| 4 | 2714.8 | 415.8 | 0.3047 | 0.0382 |

At K=4, the average visited-node count was approximately **84.7% lower**
with alpha-beta pruning. Importantly, the root minimax value was checked to
be equal with and without pruning. The CSV is in
`benchmarks/results/student_a_baseline_k_analysis.csv`; the charts are
`time_vs_k.png` and `nodes_vs_k.png` alongside it.

**Before submission:** Re-run the experiment with the final selected heuristic,
preferably on the team's target hardware. State the machine and Python version,
add measured larger K values only if they actually completed, and replace or
clearly distinguish these provisional pilot results. Do not present the
baseline heuristic as your teammate's finished composite heuristic.

## 7. Assumptions and design decisions

1. Board dimensions are fixed at **6 rows × 7 columns** as permitted by the task.
2. Four-in-a-rows are counted as separate **consecutive 4-cell windows**;
   overlapping wins count separately (a five-disc sequence contains two fours).
3. Gameplay continues until **all board cells are occupied**. The winner is
   the player with more completed windows; equal totals yield a draw.
4. The human moves first by default, but the controller permits the AI to start.
5. The AI uses MAX and the human uses MIN; positive evaluation means computer
   advantage. Full-board utility is exactly the final score difference.
6. Internally columns are zero-based; interfaces should display one-based
   column labels. Search moves are center-first with first-seen tie-breaking.
7. The minimax tree records evaluated nodes and marked pruned siblings, while
   search counters count **visited** nodes only.
8. Ordinary score-difference is sufficient to verify engine correctness; the
   final team heuristic may combine score, candidate windows, positional
   control and immediate threats, as implemented by the heuristic teammate.
