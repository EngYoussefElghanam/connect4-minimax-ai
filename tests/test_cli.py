"""Scripted-stdin tests for the console loop (the only place that uses input())."""
import itertools

import pytest

from connect4 import config
from connect4.ai.difficulty import Difficulty, k_for_difficulty
from connect4.ai.heuristics.score_diff import ScoreDifferenceHeuristic
from connect4.game import Game
from connect4.ui.console import cli


def feed(monkeypatch, answers):
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda *_a, **_k: next(it))


@pytest.mark.parametrize("choice,difficulty", [("1", Difficulty.EASY), ("2", Difficulty.MEDIUM),
                                               ("3", Difficulty.HARD)])
def test_difficulty_menu_returns_k(monkeypatch, choice, difficulty):
    feed(monkeypatch, [choice])
    assert cli.prompt_difficulty_and_k() == k_for_difficulty(difficulty)


def test_menu_reprompts_on_garbage(monkeypatch):
    feed(monkeypatch, ["??", "", "1"])
    assert cli.prompt_difficulty_and_k() == k_for_difficulty(Difficulty.EASY)


def test_custom_k_flow_reprompts_until_valid(monkeypatch):
    feed(monkeypatch, ["4", "0", "abc", str(config.MAX_K + 1), "3"])
    assert cli.prompt_difficulty_and_k() == 3


def test_prompt_human_move_reprompts_and_converts(monkeypatch):
    feed(monkeypatch, ["9", "x", "4"])
    g = Game(k=1, heuristic=ScoreDifferenceHeuristic())
    assert cli.prompt_human_move(g) == 3


@pytest.mark.timeout(120)
def test_full_scripted_game_prints_tree_and_final_result(monkeypatch, capsys):
    answers = itertools.cycle(["1", "2", "3", "4", "5", "6", "7"])
    monkeypatch.setattr("builtins.input", lambda *_a, **_k: next(answers))
    cli.run_console_game(k=1, heuristic_name="score_diff")
    out = capsys.readouterr().out
    assert "MAX" in out and "MIN" in out        # minimax tree was printed
    assert "Computer" in out                     # scoreboard / final result mentions the computer
