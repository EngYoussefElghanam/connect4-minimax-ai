"""Board representation.

Conventions (tests rely on these):
  * grid[row][col], row 0 is the TOP row, row ROWS-1 is the BOTTOM row.
  * Columns are 0-based internally (the UI converts from/to 1-based).
  * Cell values come from config: EMPTY, HUMAN, AI.
  * String form: one string per row, top to bottom, '.' empty, 'H' human, 'A' AI.
"""
from __future__ import annotations

from connect4 import config


class Board:
    def __init__(self, rows: int = config.ROWS, cols: int = config.COLS) -> None:
        """Create an empty rows x cols board."""
        # TODO: store rows, cols and an empty grid
        raise NotImplementedError

    # ---- construction / conversion ----------------------------------------
    @classmethod
    def from_strings(cls, rows: list[str]) -> "Board":
        """Build a board from top-to-bottom strings ('.', 'H', 'A'). Used heavily by tests."""
        # TODO: validate equal row lengths and legal characters
        raise NotImplementedError

    def to_strings(self) -> list[str]:
        """Inverse of from_strings."""
        # TODO
        raise NotImplementedError

    def copy(self) -> "Board":
        """Independent deep copy (minimax must never mutate the caller's board)."""
        # TODO
        raise NotImplementedError

    def swapped(self) -> "Board":
        """Copy of the board with HUMAN and AI discs exchanged (used to test heuristic symmetry)."""
        # TODO
        raise NotImplementedError

    # ---- queries -----------------------------------------------------------
    @property
    def rows(self) -> int:
        # TODO
        raise NotImplementedError

    @property
    def cols(self) -> int:
        # TODO
        raise NotImplementedError

    def get(self, row: int, col: int) -> int:
        """Value at (row, col)."""
        # TODO
        raise NotImplementedError

    def is_valid_move(self, col: int) -> bool:
        """True if col is in range and not full."""
        # TODO
        raise NotImplementedError

    def valid_moves(self) -> list[int]:
        """Playable columns, ascending order."""
        # TODO
        raise NotImplementedError

    def is_full(self) -> bool:
        # TODO
        raise NotImplementedError

    def count_pieces(self, player: int | None = None) -> int:
        """Discs of `player`, or all discs when player is None."""
        # TODO
        raise NotImplementedError

    def next_open_row(self, col: int) -> int | None:
        """Row index a disc dropped in col would land on, or None if column is full."""
        # TODO
        raise NotImplementedError

    # ---- mutation ----------------------------------------------------------
    def drop_piece(self, col: int, player: int) -> int:
        """Drop a disc in col (mutates). Returns the row it landed on.
        Raises ValueError for an invalid / full column."""
        # TODO
        raise NotImplementedError

    def with_move(self, col: int, player: int) -> "Board":
        """Return a NEW board with the move applied (handy for generating children)."""
        # TODO
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        # TODO
        raise NotImplementedError

    def __hash__(self) -> int:
        # TODO: needed if you add a transposition table later
        raise NotImplementedError
