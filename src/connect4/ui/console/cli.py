"""Console game loop. The only console module that calls input()/print().

input()/print() are looked up when called (not bound as default arguments) so
tests can monkeypatch builtins.input.
"""
from __future__ import annotations

from connect4 import config
from connect4.ai.difficulty import k_for_difficulty
from connect4.ai.heuristics import ALL_HEURISTICS, get_heuristic
from connect4.ai.minimax import SearchResult
from connect4.game import Game, GameResult
from connect4.ui.console.input_parsing import (
    parse_column_input,
    parse_difficulty_choice,
    parse_k_input,
)
from connect4.ui.console.renderer import render_board, render_scores, render_stats
from connect4.ui.console.tree_printer import format_tree, write_tree_to_file


class QuitGame(Exception):
    """Raised when the human types q/quit."""


def prompt_difficulty_and_k() -> int:
    """Menu (Easy / Medium / Hard / Custom K); loops until valid; returns K."""
    print("Choose difficulty:")
    for number, name in (("1", "Easy"), ("2", "Medium"), ("3", "Hard")):
        print(f"  {number}) {name} (K={k_for_difficulty(parse_difficulty_choice(number))})")
    print("  4) Custom K")
    while True:
        try:
            difficulty = parse_difficulty_choice(input("Difficulty> "))
        except ValueError:
            print("Please type 1, 2, 3, 4 or easy/medium/hard/custom.")
            continue
        if difficulty is not None:
            return k_for_difficulty(difficulty)
        while True:
            try:
                return parse_k_input(input(f"K (>= {config.MIN_K})> "))
            except ValueError as exc:
                print(f"Invalid K: {exc}")


def prompt_heuristic() -> str:
    """List the registered heuristics; return the chosen registry name."""
    names = sorted(ALL_HEURISTICS)
    print("Choose heuristic:")
    for i, name in enumerate(names, start=1):
        print(f"  {i}) {name}")
    while True:
        raw = input("Heuristic> ").strip().lower()
        if raw.isdigit() and 1 <= int(raw) <= len(names):
            return names[int(raw) - 1]
        if raw in ALL_HEURISTICS:
            return raw
        print(f"Type a number 1-{len(names)} or a name.")


def prompt_human_move(game: Game) -> int:
    """Ask until a legal column is entered; return it 0-based. q/quit aborts."""
    board = game.board
    while True:
        raw = input(f"Your move (1-{board.cols}, q to quit)> ")
        if raw.strip().lower() in {"q", "quit"}:
            raise QuitGame
        try:
            col = parse_column_input(raw, board.cols)
        except ValueError as exc:
            print(f"Invalid move: {exc}")
            continue
        if not board.is_valid_move(col):
            print(f"Column {col + 1} is full.")
            continue
        return col


def print_computer_turn(game: Game, result: SearchResult, tree_depth: int | None = None,
                        show_tree: bool = True) -> None:
    """Print the chosen column, the minimax tree and the search stats."""
    print(f"Computer plays column {result.column + 1} (minimax value {result.value:g})")
    if show_tree and result.tree is not None:
        print(format_tree(result.tree, max_depth=tree_depth, show_boards=True))
    s = result.stats
    print(render_stats(s.nodes_expanded, s.elapsed_seconds, s.prunes))


def run_console_game(k: int | None = None, heuristic_name: str | None = None,
                     human_starts: bool = True, use_pruning: bool = True,
                     tree_file: str | None = None,
                     tree_depth: int | None = None) -> GameResult | None:
    """Whole session: setup prompts (skipped for args already given), play until the
    board is full, print final scores and the winner. Returns None if the human quit.

    The tree is printed after every computer move (down to tree_depth if given).
    tree_file receives the tree of the computer's LAST move.
    """
    if k is None:
        k = prompt_difficulty_and_k()
    if heuristic_name is None:
        heuristic_name = prompt_heuristic()
    game = Game(k, get_heuristic(heuristic_name), human_starts=human_starts,
                use_pruning=use_pruning)
    try:
        while not game.is_over():
            print()
            print(render_board(game.board))
            print(render_scores(*game.scores()))
            if game.current_player == config.HUMAN:
                game.human_move(prompt_human_move(game))
            else:
                result = game.computer_move()
                print_computer_turn(game, result, tree_depth)
                if tree_file and result.tree is not None:
                    write_tree_to_file(result.tree, tree_file, show_boards=True)
    except QuitGame:
        print("Game aborted.")
        return None

    print()
    print(render_board(game.board))
    print(render_scores(*game.scores()))
    final = game.result()
    if final.winner == config.HUMAN:
        print("You win!")
    elif final.winner == config.AI:
        print("The computer wins.")
    else:
        print("It's a tie.")
    return final
