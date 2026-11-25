"""Integration tests for the interactive quiz."""

import json
import logging
import os
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterator, NoReturn

import pytest

from main import main
from quiz_engine import QuizEngine, SequentialMode
from ui import run_quiz, show_feedback
from utils.diagnostic_logging import DailyLogHandler, prepare_log_directory

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def isolate_log_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Keep in-process CLI tests from writing to the user's home directory."""
    monkeypatch.setattr("main.Path.home", lambda: tmp_path)


@pytest.fixture
def capture_quiz_logs(caplog: pytest.LogCaptureFixture) -> Iterator[None]:
    """Capture application logs without changing propagation."""
    logger = logging.getLogger("flashcard_quizzer")
    logger.addHandler(caplog.handler)
    try:
        yield
    finally:
        logger.removeHandler(caplog.handler)


@pytest.mark.parametrize("verbose", [False, True])
def test_diagnostic_logging(
    verbose: bool,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
    capture_quiz_logs: None,
) -> None:
    """Check logged paths and card data with and without verbose mode.

    Also checks that one unrelated environment-variable value is absent. Uses
    mocked input; does not prove all secrets are excluded from logs.
    """
    deck = tmp_path / "deck.json"
    deck_data = '[{"front": "question", "back": "answer"}]'
    deck.write_text(deck_data, encoding="utf-8")
    history = tmp_path / "history.json"
    monkeypatch.setattr("main.history_path", lambda path: history)
    monkeypatch.setattr("builtins.input", lambda prompt: "submitted")
    monkeypatch.setenv("FLASHCARD_TEST_SECRET", "unrelated-private-token")
    args = ["-f", str(deck)] + (["--verbose"] if verbose else [])

    assert main(args) == 0
    output = capsys.readouterr()
    messages = [record.getMessage() for record in caplog.records]
    assert any(str(deck) in message for message in messages)
    assert any(str(history) in message for message in messages)
    card_log = "Card: front='question', back='answer', answer='submitted'"
    assert card_log in messages
    assert "unrelated-private-token" not in "\n".join(messages)
    assert any(record.levelno == logging.INFO for record in caplog.records)
    has_debug = any(r.levelno == logging.DEBUG for r in caplog.records)
    assert has_debug == verbose
    assert "Incorrect." in output.out
    assert "question" in output.err
    log_dir = tmp_path / ".flashcard_quizzer" / "logs"
    log_files = list(log_dir.glob("quiz-*.log"))
    assert len(log_files) == 1
    persisted = log_files[0].read_text(encoding="utf-8")
    assert card_log in persisted
    assert "unrelated-private-token" not in persisted
    assert ("DEBUG Debug: selected quiz mode" in persisted) == verbose


def test_log_retention_preserves_boundary_and_unrelated_files(
    tmp_path: Path,
) -> None:
    """Expire only fully aged daily files, leaving boundary and unrelated data.

    Uses fixed UTC dates; does not test a real scheduler or file permissions.
    """
    logs = tmp_path / "logs"
    logs.mkdir()
    names = [
        "quiz-2026-01-01.log",
        "quiz-2026-01-02.log",
        "quiz-2026-02-01.log",
        "quiz-2026-01-00.log",
        "other-2026-01-01.log",
    ]
    for name in names:
        (logs / name).write_text("data", encoding="utf-8")
    (logs / "quiz-2025-01-01.log").mkdir()

    prepare_log_directory(logs, date(2026, 2, 1))

    assert not (logs / names[0]).exists()
    assert all((logs / name).exists() for name in names[1:])
    assert (logs / "quiz-2025-01-01.log").is_dir()


def test_cli_cleans_expired_logs_at_startup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Run startup cleanup before deck loading while preserving quiz history.

    Uses an isolated directory and fixed date; does not test real permissions.
    """

    class FixedDateTime:
        @staticmethod
        def now(tz: object = None) -> datetime:
            return datetime(2026, 2, 1, tzinfo=timezone.utc)

    monkeypatch.setattr("main.datetime", FixedDateTime)
    home = tmp_path / ".flashcard_quizzer"
    logs = home / "logs"
    logs.mkdir(parents=True)
    expired = logs / "quiz-2026-01-01.log"
    boundary = logs / "quiz-2026-01-02.log"
    history = home / "history.json"
    for path in (expired, boundary, history):
        path.write_text("data", encoding="utf-8")

    assert main(["-f", str(tmp_path / "missing.json")]) == 1
    assert not expired.exists()
    assert boundary.read_text(encoding="utf-8") == "data"
    assert history.read_text(encoding="utf-8") == "data"


def test_log_handler_uses_record_utc_date(tmp_path: Path) -> None:
    """Write records across UTC midnight into separate dated files.

    Uses constructed log records; does not test simultaneous processes.
    """
    handler = DailyLogHandler(tmp_path)
    for timestamp in ("2026-01-01T23:59:59", "2026-01-02T00:00:00"):
        record = logging.LogRecord(
            "test",
            logging.INFO,
            "",
            0,
            timestamp,
            (),
            None,
        )
        utc_time = datetime.fromisoformat(timestamp)
        utc_time = utc_time.replace(tzinfo=timezone.utc)
        record.created = utc_time.timestamp()
        handler.handle(record)
    first = (tmp_path / "quiz-2026-01-01.log").read_text(encoding="utf-8")
    second = (tmp_path / "quiz-2026-01-02.log").read_text(encoding="utf-8")
    assert "2026-01-01T23:59:59Z INFO" in first
    assert "2026-01-02T00:00:00Z INFO" in second


def test_log_write_failure_warns_once(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Warn once when file writes fail without raising or retrying.

    Uses a missing directory rather than simulating OS-specific permissions.
    """
    handler = DailyLogHandler(tmp_path / "missing")
    record = logging.LogRecord("test", logging.INFO, "", 0, "test", (), None)
    handler.handle(record)
    handler.handle(record)
    assert capsys.readouterr().err.count("Cannot write diagnostic log") == 1


def test_log_cleanup_failure_stops_quiz(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Report a startup cleanup failure and do not load a deck.

    Simulates permission denial without testing actual filesystem ACLs.
    """

    def fail_cleanup(directory: Path, today: date) -> NoReturn:
        raise PermissionError("access denied")

    def fail_load(path: str) -> NoReturn:
        pytest.fail("deck must not load after log cleanup fails")

    monkeypatch.setattr("main.prepare_log_directory", fail_cleanup)
    monkeypatch.setattr("main.load_flashcards", fail_load)
    assert main(["-f", "deck.json"]) == 1
    stderr = capsys.readouterr().err
    assert "Cannot prepare diagnostic logs: access denied" in stderr


@pytest.mark.parametrize("verbose", [False, True])
@pytest.mark.parametrize("failure", ["deck", "history", "unexpected"])
def test_logging_reports_failure_once(
    verbose: bool,
    failure: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
    capsys: pytest.CaptureFixture[str],
    capture_quiz_logs: None,
) -> None:
    """Check one error record for deck, history, and runtime errors.

    Checks the friendly error and verbose-only traceback; it does not test
    every failure type, real permissions, or terminal signals.
    """
    deck = tmp_path / "missing.json"
    expected = "Error: File not found:"
    if failure == "history":
        deck.write_text('[{"front": "q", "back": "a"}]', encoding="utf-8")
        history = tmp_path / "history.json"
        history.write_text("{", encoding="utf-8")
        monkeypatch.setattr("main.history_path", lambda path: history)
        expected = "Error: Cannot read history"
    elif failure == "unexpected":

        def fail_load(path: str) -> NoReturn:
            raise RuntimeError("unexpected failure")

        monkeypatch.setattr("main.load_flashcards", fail_load)
        expected = "Error: Unexpected RuntimeError:"
    args = ["-f", str(deck)]
    if verbose:
        args.append("--verbose")
    assert main(args) == 1
    stderr = capsys.readouterr().err
    errors = [r for r in caplog.records if r.levelno == logging.ERROR]
    assert len(errors) == 1
    lines = stderr.splitlines()
    assert sum(line.startswith(expected) for line in lines) == 1
    assert ("Traceback" in stderr) == verbose
    assert bool(errors[0].exc_info) == verbose
    log_dir = tmp_path / ".flashcard_quizzer" / "logs"
    log_file = next(log_dir.glob("quiz-*.log"))
    assert ("Traceback" in log_file.read_text(encoding="utf-8")) == verbose


def test_adaptive_history_survives_separate_processes(tmp_path: Path) -> None:
    """Run two CLI processes and prioritize a previously missed card.

    Checks saved-miss display, adaptive order, and early-exit question count;
    it does not inspect saved history after the second process or concurrency.
    """
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
    """Exercise scoring, saved misses, and adaptive ordering across sessions.

    Uses mocked input and history location; does not test real terminal signals
    or all adaptive tie cases.
    """
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
    """Simulate Ctrl+C and EOF before the first answer.

    Checks the exit message, zero-question summary, and no history file; it
    does not send actual terminal signals or interrupt history writes.
    """
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
    """Simulate an interrupt after one incorrect completed answer.

    Checks that one miss remains saved and the summary counts one answer;
    it does not test interruption during a write or real terminal signals.
    """
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
    """Reprompt for empty and whitespace-only answers before a correct answer.

    Checks two warnings and an unaffected one-question score; it does not cover
    other input sequences or a real terminal.
    """
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
    """Return a friendly error when the saved history contains invalid JSON.

    Checks a nonzero return value, stderr fragment, and no traceback; it does
    not exercise history-write failures or a separate CLI process.
    """
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
    """Check feedback color codes on a simulated TTY and NO_COLOR behavior.

    Does not verify actual terminal rendering, redirected output, or NO_COLOR
    behavior for incorrect answers.
    """
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
