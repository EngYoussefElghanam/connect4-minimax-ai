"""Entry point.

    python main.py                          # console, asks for difficulty / K interactively
    python main.py --difficulty hard
    python main.py --k 5 --heuristic composite
    python main.py --gui
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))


def build_parser() -> argparse.ArgumentParser:
    """Define --gui, --difficulty, --k, --heuristic, --no-pruning, --ai-first."""
    # TODO
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Parse args, then dispatch to ui.console.cli.run_console_game or ui.gui.app.run_gui.
    --k and --difficulty are mutually exclusive; with neither, the UI prompts."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
