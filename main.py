"""Entry point.

    python main.py                          # console, asks for difficulty / K interactively
    python main.py --difficulty hard
    python main.py --k 5 --heuristic composite
    python main.py --gui
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from connect4.ai.difficulty import (  # noqa: E402
    Difficulty,
    difficulty_from_name,
    k_for_difficulty,
    validate_k,
)
from connect4.ai.heuristics import ALL_HEURISTICS  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Connect 4 against a minimax AI")
    parser.add_argument("--gui", action="store_true", help="open the pygame GUI")
    level = parser.add_mutually_exclusive_group()
    level.add_argument("--difficulty", choices=[d.name.lower() for d in Difficulty])
    level.add_argument("--k", "-k", type=int, help="search depth")
    parser.add_argument("--heuristic", choices=sorted(ALL_HEURISTICS))
    parser.add_argument("--no-pruning", action="store_true",
                        help="plain minimax without alpha-beta pruning")
    parser.add_argument("--ai-first", action="store_true", help="computer moves first")
    parser.add_argument("--tree-file", help="console: save the last search tree here")
    parser.add_argument("--show-tree-depth", type=int,
                        help="console: print the tree only down to this depth")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    k = None
    try:
        if args.k is not None:
            k = validate_k(args.k)
        elif args.difficulty:
            k = k_for_difficulty(difficulty_from_name(args.difficulty))
    except ValueError as exc:
        parser.error(str(exc))

    if args.gui:
        from connect4.ui.gui.app import run_gui  # lazy: console mode needs no pygame

        run_gui(k=k, heuristic_name=args.heuristic, human_starts=not args.ai_first,
                use_pruning=not args.no_pruning)
        return 0

    from connect4.ui.console.cli import run_console_game

    run_console_game(k, args.heuristic, human_starts=not args.ai_first,
                     use_pruning=not args.no_pruning, tree_file=args.tree_file,
                     tree_depth=args.show_tree_depth)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
