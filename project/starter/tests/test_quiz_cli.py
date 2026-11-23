"""Integration tests for the interactive quiz."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from main import main
from quiz_engine import QuizEngine, SequentialMode
from ui import run_quiz, show_feedback

ROOT = Path(__file__).resolve().parents[1]


def test_adaptive_history_survives_separate_processes(tmp_path: Path) -> None:
    deck = tmp_path / "deck.json"
    deck.write_text(
        '[{"front": "one", "back": "1"}, {"front": "two", "back": "2"}]',
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    env["USERPROFILE"] = str(tmp_path)
    command = [sys.executable, str(ROOT / "main.py"), "-f", str(deck)]
    first = subprocess.run(
        command, input="1\nwrong\n", text=True, capture_output=True, env=env
    )
    assert first.returncode == 0
    second = subprocess.run(
        command + ["-m", "adaptive", "--stats"],
        input="2\nexit\n",
        text=True,
        capture_output=True,
        env=env,
    )
    assert second.returncode == 0
    assert "two: 1 missed" in second.stdout
    assert second.stdout.index("\ntwo\n") < second.stdout.index("\none\n")
    assert "Total Questions | 1" in second.stdout


def test_adaptive_history_and_stats_across_sessions(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    deck = tmp_path / "deck.json"
    deck.write_text(
        json.dumps(
            [
                {"front": "one", "back": "first"},
                {"front": "two", "back": "second"},
            ]
        ),
        encoding="utf-8",
    )
    history = tmp_path / "history.json"
    monkeypatch.setattr("main.history_path", lambda path: history)
    answers = iter(["first", "wrong"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    assert main(["-f", str(deck)]) == 0
    output = capsys.readouterr().out
    assert "Correct!" in output and "Incorrect." in output
    assert "Total Questions | 2" in output
    assert "Accuracy %      | 50.0%" in output
    assert "Missed terms    | two" in output

    answers = iter(["SECOND", "exit"])
    assert main(["-f", str(deck), "-m", "adaptive", "--stats"]) == 0
    output = capsys.readouterr().out
    assert "two: 1 missed" in output
    assert output.index("\ntwo\n") < output.index("\none\n")
    assert "Total Questions | 1" in output
    assert "Accuracy %      | 100.0%" in output
    assert json.loads(history.read_text(encoding="utf-8")) == {}


@pytest.mark.parametrize("error", [KeyboardInterrupt, EOFError])
def test_quit_gracefully_on_interrupt_or_eof(
    error: type[BaseException],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    engine = QuizEngine([{"front": "one", "back": "1"}], SequentialMode(), {})

    def quit_input(prompt: str) -> str:
        raise error()

    monkeypatch.setattr("builtins.input", quit_input)
    run_quiz(engine, tmp_path / "history.json")
    output = capsys.readouterr().out
    assert "Quiz ended." in output
    assert "Total Questions | 0" in output
    assert not (tmp_path / "history.json").exists()


def test_interrupt_keeps_completed_answers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    engine = QuizEngine(
        [{"front": "one", "back": "1"}, {"front": "two", "back": "2"}],
        SequentialMode(),
        {},
    )
    answers = iter(["wrong"])

    def answer_then_interrupt(prompt: str) -> str:
        try:
            return next(answers)
        except StopIteration:
            raise KeyboardInterrupt

    monkeypatch.setattr("builtins.input", answer_then_interrupt)
    path = tmp_path / "history.json"
    run_quiz(engine, path)
    assert list(json.loads(path.read_text(encoding="utf-8")).values()) == [1]
    assert "Total Questions | 1" in capsys.readouterr().out


def test_blank_answers_are_reprompted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    engine = QuizEngine([{"front": "one", "back": "1"}], SequentialMode(), {})
    answers = iter(["", "  ", "1"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    run_quiz(engine, tmp_path / "history.json")
    output = capsys.readouterr().out
    assert output.count("Answer cannot be empty") == 2
    assert "Total Questions | 1" in output
    assert "Accuracy %      | 100.0%" in output
    assert engine.stats.missed == []


def test_cli_reports_history_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    deck = tmp_path / "deck.json"
    deck.write_text('[{"front": "one", "back": "1"}]', encoding="utf-8")
    history = tmp_path / "history.json"
    history.write_text("invalid", encoding="utf-8")
    monkeypatch.setattr("main.history_path", lambda path: history)
    assert main(["-f", str(deck)]) == 1
    error = capsys.readouterr().err
    assert "Cannot read history" in error
    assert "Traceback" not in error


def test_feedback_color_and_no_color(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr("sys.stdout.isatty", lambda: True)
    monkeypatch.delenv("NO_COLOR", raising=False)
    show_feedback(True, "answer")
    show_feedback(False, "answer")
    output = capsys.readouterr().out
    assert "\033[32mCorrect!" in output
    assert "\033[31mIncorrect." in output
    monkeypatch.setenv("NO_COLOR", "1")
    show_feedback(True, "answer")
    assert "\033[" not in capsys.readouterr().out
