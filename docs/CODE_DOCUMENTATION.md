# Connect 4 Minimax: Code Documentation

This document explains every class and function in the modules below, followed by a glossary of the less common Python syntax used in them.

**Conventions used throughout the code**

- Rows are indexed **top to bottom** (row 0 is the top row); columns are zero-based.
- Cell values are integers from `config`: `EMPTY = 0`, `HUMAN = 1`, `AI = 2`.
- The AI is the **maximizer** and the human is the **minimizer**. A positive evaluation means the AI is better, a negative one means the human is better.
- The game ends **only when the board is full**. The winner is whoever completed more four-cell windows.

---

## 1. `config.py`

Global constants only, with no functions. Every tunable number lives here so the report can cite one place.

| Constant | Meaning |
|---|---|
| `ROWS`, `COLS` | Board size (6 x 7). |
| `CONNECT` | Discs needed for one "connected four" (4). |
| `EMPTY`, `HUMAN`, `AI` | Integer codes for cell contents. |
| `MIN_K`, `MAX_K` | Allowed search depth range (1 to 10). |
| `DIFFICULTY_K` | Maps difficulty name to search depth (`EASY`=2, `MEDIUM`=4, `HARD`=6). |
| `HEURISTIC_WEIGHTS` | Weights used by `CompositeHeuristic` for each sub-heuristic. |

---

## 2. `board.py`: `Board`

A mutable grid with gravity. Child positions are independent copies, so searching never corrupts the real game board.

### `Board.__init__(rows=config.ROWS, cols=config.COLS)`
Creates an empty board. It rejects non-integer or non-positive sizes with `ValueError`. It uses `type(rows) is not int` rather than `isinstance`, so `True`/`False` (which are `int` subclasses) are rejected. The grid is a list of lists built with a nested list comprehension.

### `Board.from_strings(rows)` (classmethod)
Builds a board from a list of strings such as `["....", "H.A."]`, where `.` is empty, `H` is human and `A` is AI.
- Validates that the list is non-empty, every row is a string of the same length, and only `.`, `H`, `A` appear.
- **Does not check gravity**, so floating discs are allowed. This is intentional so test fixtures and scoring diagrams can be arbitrary.
- Creates the object with `cls(len(rows), width)` and then overwrites `_grid`.

### `Board.to_strings()`
The inverse of `from_strings`. It returns one string per row using `.`, `H`, `A`.

### `Board.copy()`
Returns a new `Board` with a deep-enough copy of the grid. `row.copy()` copies each inner list, so the clone shares no mutable state with the original.

### `Board.swapped()`
Returns a copy with every `HUMAN` disc turned into `AI` and vice versa (empties unchanged). Tests use it to check that heuristics are symmetric: `evaluate(b) == -evaluate(b.swapped())`.

### `Board.rows` / `Board.cols` (properties)
Read-only access to the private `_rows` / `_cols`.

### `Board.get(row, col)`
Returns the cell value at that position. No bounds checking beyond Python's list indexing (negative indices wrap around).

### `Board.is_valid_move(col)`
True if `col` is an integer in range **and** the top cell of that column (`_grid[0][col]`) is empty, meaning the column is not full. `type(col) is int` rejects bools and floats.

### `Board.valid_moves()`
List of all playable columns, left to right.

### `Board.is_full()`
True when there are no valid moves. In this game this is the **only terminal state**.

### `Board.count_pieces(player=None)`
Counts discs. With `player=None` it counts all non-empty cells; otherwise it counts only that player's discs. It raises `ValueError` for an invalid player. It sums booleans, since `True == 1` (see glossary).

### `Board.next_open_row(col)`
Returns the row index where a disc dropped in `col` would land: the lowest empty row, found by scanning from the bottom (`range(rows-1, -1, -1)`). It returns `None` if the column is out of range or full.

### `Board.drop_piece(col, player)`
Mutates the board: validates the player and column, finds the landing row, places the disc and returns the row index. The `assert row is not None` documents an invariant, because after `is_valid_move` passes on a gravity-valid board a row must exist.

### `Board.with_move(col, player)`
Non-mutating version of `drop_piece`: copies the board, drops the disc on the copy and returns it. Minimax uses this to create child positions.

### `Board.__eq__(other)`
Two boards are equal if they have the same dimensions and grid contents. It returns `False` for non-`Board` objects.

### `Board.__hash__()`
Hash built from the dimensions and an immutable tuple-of-tuples snapshot of the grid, so boards can be dict/set keys. Defining `__eq__` removes the default hash, so it must be redefined. Do not mutate a board after using it as a key.

---

## 3. `scoring.py`: window-based scoring

The game score is the number of four-cell windows owned by a player. **Overlapping windows each count**, so five in a row counts as two fours.

### `iter_windows(board)` (generator)
Yields every length-4 window on the board as a list of `(row, col)` coordinates.
- `directions = ((0,1), (1,0), (1,1), (-1,1))` means horizontal, vertical (downward), diagonal down-right and diagonal up-right. Each window starts at a cell and extends in only one direction, so no window is produced twice.
- The end cell is computed first (`start + 3 * direction`), and the window is yielded only if the end cell is on the board.
- It uses `yield`, so windows are produced one at a time instead of being stored in a big list (see glossary).

### `count_connect_fours(board, player)`
Counts windows in which all four cells belong to `player`. It validates the player. `all(...)` checks one window, and `sum(...)` over booleans counts the true ones.

### `get_scores(board)`
Returns the tuple `(human_score, ai_score)`.

### `score_difference(board)`
Returns `ai - human`. Positive means the AI is ahead. This is the exact final utility used on full boards.

### `winner(board)`
Returns `config.AI` if the difference is positive, `config.HUMAN` if negative and `None` for a tie. It uses a chained conditional expression (see glossary).

---

## 4. `ai/difficulty.py`

### `Difficulty` (Enum)
Three members, `EASY`, `MEDIUM` and `HARD`, whose values equal their names so they can be used as keys of `config.DIFFICULTY_K`.

### `validate_k(k)`
Returns `k` unchanged if it is an `int` (not a bool) within `[MIN_K, MAX_K]`; otherwise raises `ValueError`. The chained comparison `config.MIN_K <= k <= config.MAX_K` is standard Python.

### `k_for_difficulty(difficulty)`
Looks up the depth for a `Difficulty` member and validates it. It raises `ValueError` if the argument isn't a `Difficulty`.

### `difficulty_from_name(name)`
Converts a string such as `" hard "` into `Difficulty.HARD` using `strip().upper()` and `Difficulty[...]` (lookup by member name). A `KeyError` is converted into a `ValueError` with `raise ... from exc`, which keeps the original error attached as the cause.

---

## 5. `ai/stats.py`: `SearchStats`

A `@dataclass` holding counters for one search: `nodes_expanded`, `leaf_evaluations`, `prunes`, `elapsed_seconds`, `max_depth_reached`.

### `SearchStats.reset()`
Sets every counter back to zero. `MinimaxAgent` calls it at the start of each search.

---

## 6. `ai/tree.py`: the captured search tree

### `TreeNode` (dataclass)
One node of the search tree.

| Field | Meaning |
|---|---|
| `depth` | Distance from the root (root = 0). |
| `is_max` | True if the AI (maximizer) moves at this node. |
| `move` | Column that led to this node (`None` for the root). |
| `board` | Optional board snapshot. |
| `value` | Minimax value of the node. |
| `is_leaf` | True if the node was evaluated directly. |
| `pruned` | True for placeholder nodes that alpha-beta skipped. |
| `alpha`, `beta` | Alpha-beta window when the node finished. |
| `heuristic_breakdown` | Per-factor leaf score, for display. |
| `children` | Child nodes. Uses `field(default_factory=list)` so every node gets its own list. |

### `iter_nodes(root)` (generator)
Preorder depth-first traversal: yields the node, then recursively yields all nodes of each child from left to right. It uses `yield from` to delegate to the recursive call.

### `count_nodes(root, include_pruned=True)`
Counts nodes in the tree. With `include_pruned=False` the pruned placeholders are excluded.

### `tree_depth(root)`
Returns the greatest `depth` value among all nodes.

---

## 7. `ai/heuristics/`

All heuristics share one interface and return **weighted per-factor contributions** in a dict, so the UI can show why a leaf got its score.

### 7.1 `base.py`

#### `window_counts(board)` (generator)
For every 4-cell window yields `(cells, ai_count, human_count)`. It reads the values of the window's cells into a list and uses `list.count` for each player. Empty cells are not counted.

#### `Heuristic` (abstract base class)
- `name`: string label used by subclasses.
- `__init__(weight=1.0)`: stores a global multiplier for this heuristic.
- `breakdown(board)`: **abstract**. Subclasses must return a `dict[str, float]` of already-weighted contributions.
- `evaluate(board)`: returns `sum(breakdown(board).values())`. Because it is defined this way, the breakdown always adds up to the evaluation.

**Sign convention:** positive favors the AI, negative favors the human, and `evaluate(b) == -evaluate(b.swapped())`.

### 7.2 `score_diff.py`: `ScoreDifferenceHeuristic`
`breakdown(board)`: `{"score_diff": weight * (AI fours - human fours)}`. This is the real game objective applied to a partial board.

### 7.3 `open_windows.py`: `OpenWindowsHeuristic`
Rewards windows that one player can still complete.
- `DISC_POINTS = {1: 1, 2: 5, 3: 20}` gives points for a window holding that many of a player's discs.
- `breakdown(board)`: for each window, if the human has 0 discs and the AI has 1 to 3, the AI earns the matching points; symmetrically for the human. Windows containing both players' discs are dead and score nothing. `ai in DISC_POINTS` tests dictionary keys, so 0 and 4 are excluded.
- Returns `{"ai_open_windows": +pts, "human_open_windows": -pts}`.

### 7.4 `positional.py`: `PositionalHeuristic`
Central columns take part in more windows, so discs there are worth more.
- `breakdown(board)`: for each non-empty cell, weight `w = 1 + (centre - abs(c - centre))`. On a 7-column board, edge columns are worth 1 and the centre column 4. The AI's weights are summed positively and the human's negatively.

### 7.5 `threats.py`: `ThreatHeuristic`
Counts **immediate** threats: windows with 3 discs of one player and 1 empty cell, where that empty cell can be played right now.
- `breakdown(board)`: skip windows that are not exactly 3-of-one-player and 0 of the other. For the remaining window, find its single empty cell and check `board.next_open_row(c) == r`, meaning the disc would land exactly there. The `break` stops after the empty cell is found, because there is only one.
- Returns `{"ai_threats": +n, "human_threats": -n}`.

### 7.6 `composite.py`: `CompositeHeuristic`
Weighted sum of the four heuristics above.
- `__init__(weights=None, weight=1.0)`: copies `config.HEURISTIC_WEIGHTS` (or the given dict) with `dict(...)` so later edits don't affect the config, and builds one instance of each part.
- `breakdown(board)`: returns one entry per part, `self.weight * self.weights[name] * part.evaluate(board)`.

### 7.7 `heuristics/__init__.py`: registry

#### `ALL_HEURISTICS`
Dictionary from name to heuristic **class** (not instance).

#### `get_heuristic(name)`
Looks up the class and instantiates it with default arguments. Unknown names raise `ValueError` listing the valid choices (`sorted(ALL_HEURISTICS)`). The CLI and GUI use it to list and pick heuristics by name.

---

## 8. `ai/minimax.py`: the search

### `SearchResult` (dataclass)
Return value of a search: `column` (chosen move), `value` (minimax value), `tree` (root `TreeNode` or `None`) and `stats` (a `SearchStats` snapshot).

### `MinimaxAgent.__init__(heuristic, k, use_pruning=True, record_tree=True, record_boards=True)`
Validates `k` and stores the options. `record_tree` controls whether a tree is captured, and `record_boards` controls whether each node stores a board copy (costly, so benchmarks can turn it off). `_best_root_move` is internal state set during search.

### `MinimaxAgent.choose_move(board)`
Public entry point.
1. Raises `ValueError` on a full board.
2. Resets stats and the best root move.
3. Creates the root `TreeNode` if tree recording is on.
4. Times the search with `perf_counter()` and calls `_search` with the full window `(-inf, +inf)`, as the maximizer, at depth 0.
5. Takes a **snapshot** of the statistics with `SearchStats(**vars(self.stats))`, so later searches cannot change a past result.
6. Returns a `SearchResult`.

### `MinimaxAgent._search(board, depth, alpha, beta, maximizing, node)`
Recursive K-ply minimax with optional alpha-beta pruning.

- **Counting:** every call increments `nodes_expanded` and updates `max_depth_reached`.
- **Leaf test:** if `depth == k` or the board is full, it evaluates the board via `_evaluate_leaf`, counts a leaf, and (if a tree node exists) records the value, the alpha/beta window and a heuristic breakdown. For a full board the breakdown is just `{"terminal_score_diff": value}`.
- **Interior node:** generate ordered moves, then for each column:
  1. `player` is AI when maximizing, HUMAN otherwise.
  2. Create the child board with `with_move` and, if recording, a child `TreeNode` appended to the parent.
  3. Recurse with the roles flipped (`not maximizing`).
  4. Update `best` (max for the AI, min for the human). At depth 0, remember the column in `_best_root_move`. Because the comparison is **strict** (`>` / `<`), ties keep the earlier, more central move.
  5. If pruning is enabled, update alpha (maximizer) or beta (minimizer). If `alpha >= beta`, the remaining siblings cannot change the result: count a prune, add `pruned=True` placeholder nodes for the skipped columns (`moves[index + 1:]`, not counted as expanded) and `break`.
- Finally stores `value`, `alpha` and `beta` on the node and returns `best`.

### `MinimaxAgent._evaluate_leaf(board)`
On a full board returns the exact `float(score_difference(board))`; otherwise returns `float(heuristic.evaluate(board))`.

### `MinimaxAgent._order_moves(board)`
Returns valid columns sorted center-first. The sort key is the tuple `(abs(c - middle), c)`: distance from the center, with ties broken by the lower column index. Searching strong central moves first tends to cause earlier alpha-beta cutoffs, and the ordering is deterministic.

---

## 9. `game.py`: the UI-independent controller

### `GameResult` (dataclass)
Final result: `human_score`, `ai_score`, `winner` (`HUMAN`, `AI` or `None`).

### `Game.__init__(k, heuristic, board=None, human_starts=True, use_pruning=True)`
Validates `k`, copies a supplied starting board (or creates an empty one), sets who moves first and creates a `MinimaxAgent`.

### `Game.board` / `Game.current_player` (properties)
Read-only access to the board and to whose turn it is.

### `Game.is_over()`
True when the board is full.

### `Game.human_move(col)`
Raises `ValueError` if the game is over or it is not the human's turn. Otherwise drops a human disc, switches the turn to the AI and returns the landing row.

### `Game.computer_move()`
Same checks for the AI. Runs `choose_move`, drops the chosen disc, switches the turn to the human and returns the whole `SearchResult` (so the UI can show stats and the tree).

### `Game.scores()`
Returns `(human, ai)` current scores via `get_scores`.

### `Game.result()`
Only valid when the game is over (otherwise `ValueError`). Returns a `GameResult`.

---

## 10. Glossary of unusual syntax

**`yield` (generators).** A function containing `yield` returns a *generator*: it produces values lazily, one at a time, pausing after each `yield` and resuming when the next value is requested. `iter_windows`, `window_counts` and `iter_nodes` use it so no full list of windows or nodes is built in memory. You consume a generator with a `for` loop, `sum(...)`, `all(...)`, and so on.

**`yield from other_iterable`.** Yields every item from another iterable/generator, as if you wrote `for x in other_iterable: yield x`. `iter_nodes` uses it to recurse into children.

**`from __future__ import annotations`.** Makes type hints lazy strings, so you can write `TreeNode | None` or refer to a class inside its own definition without errors, even on older Python versions.

**`X | None` type hints.** Means "either an `X` or `None`" (an optional value). `dict[str, float]` and `list[int]` are built-in generic types: a dict from strings to floats, a list of ints.

**`@dataclass`.** A decorator that auto-generates `__init__`, `__repr__` and `__eq__` from the annotated fields. `field(default_factory=list)` gives every instance its *own* new empty list (a plain `= []` default would be shared and is rejected).

**`SearchStats(**vars(self.stats))`.** `vars(obj)` returns the object's attributes as a dict; `**dict` unpacks that dict into keyword arguments. The line therefore creates a copy of the stats object.

**`@classmethod` and `cls`.** `from_strings` receives the class itself (`cls`) instead of an instance, so it works as an alternative constructor: `Board.from_strings([...])`.

**`@property`.** Lets a method be read like an attribute (`board.rows` instead of `board.rows()`), making the value read-only from outside.

**`ABC` and `@abstractmethod`.** `Heuristic` is an abstract base class: it cannot be instantiated directly, and subclasses must implement `breakdown`.

**Leading underscore (`_grid`, `_search`).** A convention meaning "internal, not part of the public API". Python does not enforce it.

**`type(x) is int` vs `isinstance`.** `isinstance(True, int)` is `True` because `bool` subclasses `int`. `type(x) is int` is stricter and rejects booleans.

**`float("inf")` / `from math import inf`.** Positive infinity, used as the initial alpha-beta bounds (`-inf`, `inf`) and as the initial `best` value.

**Chained comparisons.** `a <= b <= c` means `a <= b and b <= c`.

**Chained conditional expression.** `config.AI if diff > 0 else config.HUMAN if diff < 0 else None` evaluates like `if / elif / else` in one expression.

**Summing booleans.** `True` equals 1 and `False` equals 0, so `sum(cond for ...)` counts how many items satisfy `cond`. `count_connect_fours` and `count_pieces` rely on this.

**Generator expressions.** `(expr for x in items)` inside `sum(...)`, `all(...)` or `next(...)` is a lazy list comprehension without the brackets.

**`next(iterator, default)`.** Returns the first item of the iterator, or `default` if it is empty. `next_open_row` uses it to find the first empty row from the bottom, or `None`.

**`enumerate(moves)`.** Yields `(index, item)` pairs. `_search` uses the index to slice off the skipped siblings with `moves[index + 1:]`.

**Slicing `moves[index + 1:]`.** All elements after position `index`.

**`sorted(..., key=lambda c: (abs(c - middle), c))`.** `lambda` is an anonymous one-line function. The key returns a tuple, and tuples compare element by element, so the order is "closest to center, then smaller column".

**`for _, ai, hu in window_counts(board)`.** Tuple unpacking in a loop; `_` is the conventional name for a value you intentionally ignore.

**`raise ... from exc`.** Raises a new exception while keeping the original as its `__cause__`, so the traceback shows both.

**`assert condition`.** Raises `AssertionError` if the condition is false. It is used for internal invariants that should always hold, not for validating user input.

**`__eq__` and `__hash__`.** Special ("dunder") methods that customize `==` and `hash(obj)`. Objects that compare equal must have equal hashes, and defining `__eq__` alone would set `__hash__` to `None`.

**f-strings.** `f"column {col} is invalid"` embeds expressions inside `{}` in a string. `{name!r}` inserts the `repr()` of the value (strings appear with quotes).

**Weighted dict returns.** The heuristics return dicts such as `{"ai_threats": +n, "human_threats": -n}`, where the human's side is already negative. That is how the sign convention is built in, and it is why `evaluate` can simply sum the values.
