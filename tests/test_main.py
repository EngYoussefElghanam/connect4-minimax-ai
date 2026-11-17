import pytest

from main import build_parser


def parse(*argv):
    return build_parser().parse_args(list(argv))


def test_defaults_launch_console_with_prompts():
    a = parse()
    assert a.gui is False and a.k is None and a.difficulty is None


def test_k_flag():
    assert parse("--k", "5").k == 5


def test_difficulty_flag():
    assert parse("--difficulty", "hard").difficulty.lower() == "hard"


def test_heuristic_flag():
    assert parse("--heuristic", "composite").heuristic == "composite"


def test_gui_flag():
    assert parse("--gui").gui is True


def test_pruning_and_first_player_flags():
    a = parse("--no-pruning", "--ai-first")
    assert a.no_pruning is True and a.ai_first is True


def test_k_and_difficulty_are_mutually_exclusive():
    with pytest.raises(SystemExit):
        parse("--k", "3", "--difficulty", "easy")
