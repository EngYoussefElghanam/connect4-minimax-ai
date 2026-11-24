"""Mutable Connect 4 board with gravity and independent child positions.

Rows are indexed from top to bottom; columns are zero-based. String fixtures
are intentionally *not* gravity-validated so partial/scoring diagrams work.
"""
from __future__ import annotations

from connect4 import config


class Board:
    def __init__(self, rows: int = config.ROWS, cols: int = config.COLS) -> None:
        if type(rows) is not int or type(cols) is not int or rows < 1 or cols < 1:
            raise ValueError("rows and cols must be positive integers")
        self._rows = rows
        self._cols = cols
        self._grid = [[config.EMPTY for _ in range(cols)] for _ in range(rows)]

    @classmethod
    def from_strings(cls, rows: list[str]) -> "Board":
        if not rows or not isinstance(rows[0], str) or not rows[0]:
            raise ValueError("provide at least one nonempty board row")
        width = len(rows[0])
        if any(not isinstance(row, str) or len(row) != width for row in rows):
            raise ValueError("all board rows must have the same length")
        char_to_cell = {".": config.EMPTY, "H": config.HUMAN, "A": config.AI}
        if any(char not in char_to_cell for row in rows for char in row):
            raise ValueError("board strings must contain only '.', 'H', and 'A'")
        board = cls(len(rows), width)
        board._grid = [[char_to_cell[char] for char in row] for row in rows]
        return board

    def to_strings(self) -> list[str]:
        cell_to_char = {config.EMPTY: ".", config.HUMAN: "H", config.AI: "A"}
        return ["".join(cell_to_char[cell] for cell in row) for row in self._grid]

    def copy(self) -> "Board":
        clone = Board(self.rows, self.cols)
        clone._grid = [row.copy() for row in self._grid]
        return clone

    def swapped(self) -> "Board":
        clone = self.copy()
        clone._grid = [
            [config.AI if cell == config.HUMAN else config.HUMAN if cell == config.AI else cell
             for cell in row]
            for row in self._grid
        ]
        return clone

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def get(self, row: int, col: int) -> int:
        return self._grid[row][col]

    def is_valid_move(self, col: int) -> bool:
        return type(col) is int and 0 <= col < self.cols and self._grid[0][col] == config.EMPTY

    def valid_moves(self) -> list[int]:
        return [col for col in range(self.cols) if self.is_valid_move(col)]

    def is_full(self) -> bool:
        return not self.valid_moves()

    def count_pieces(self, player: int | None = None) -> int:
        if player is not None and player not in (config.HUMAN, config.AI):
            raise ValueError("player must be HUMAN or AI")
        return sum(
            cell != config.EMPTY if player is None else cell == player
            for row in self._grid for cell in row
        )

    def next_open_row(self, col: int) -> int | None:
        if type(col) is not int or not 0 <= col < self.cols:
            return None
        return next((row for row in range(self.rows - 1, -1, -1)
                     if self._grid[row][col] == config.EMPTY), None)

    def drop_piece(self, col: int, player: int) -> int:
        if player not in (config.HUMAN, config.AI):
            raise ValueError("player must be HUMAN or AI")
        if not self.is_valid_move(col):
            raise ValueError(f"column {col} is invalid or full")
        row = self.next_open_row(col)
        assert row is not None  # guaranteed by is_valid_move for gravity-valid boards
        self._grid[row][col] = player
        return row

    def with_move(self, col: int, player: int) -> "Board":
        child = self.copy()
        child.drop_piece(col, player)
        return child

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, Board) and self.rows == other.rows
                and self.cols == other.cols and self._grid == other._grid)

    def __hash__(self) -> int:
        # Do not mutate a Board once it is being used as a dict/set key.
        return hash((self.rows, self.cols, tuple(tuple(row) for row in self._grid)))
