"""Console game loop. This is the only console module that calls input()/print()."""
from __future__ import annotations

from connect4.game import Game


def prompt_difficulty_and_k() -> int:
    """Show the menu (Easy / Medium / Hard / Custom K), loop until valid, return K."""
    # TODO: use input_parsing.parse_difficulty_choice, k_for_difficulty, parse_k_input
    raise NotImplementedError


def prompt_heuristic() -> str:
    """List heuristics.ALL_HEURISTICS and return the chosen registry name."""
    # TODO
    raise NotImplementedError


def prompt_human_move(game: Game) -> int:
    """Ask for a column until a legal one is entered; return it 0-based."""
    # TODO
    raise NotImplementedError


def print_computer_turn(game: Game, result) -> None:
    """Print the chosen column, the full minimax tree and the search stats."""
    # TODO
    raise NotImplementedError


def run_console_game(k: int | None = None, heuristic_name: str | None = None,
                     human_starts: bool = True, use_pruning: bool = True) -> None:
    """Whole session: setup prompts (skipped for args already given) -> loop until the
    board is full -> print final scores and the winner."""
    # TODO
    raise NotImplementedError
