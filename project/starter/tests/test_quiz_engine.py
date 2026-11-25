"""Tests for quiz strategies, results, and persisted history."""

import json
from pathlib import Path

import pytest

from data_loader import Flashcard
from quiz_engine import (
    AdaptiveMode,
    QuizEngine,
    QuizModeFactory,
    RandomMode,
    SequentialMode,
    card_key,
)
from utils.history import (
    HistoryError,
    history_path,
    load_history,
    save_history,
)


@pytest.fixture
def cards() -> list[Flashcard]:
    return [
        {"front": "one", "back": "First"},
        {"front": "two", "back": "Second"},
        {"front": "three", "back": "Third"},
    ]


def test_factory_and_sequential_order(cards: list[Flashcard]) -> None:
    """Create sequential mode, preserve deck order, and reject an unknown mode.

    Does not verify all factory modes here or modifications to the input deck.
    """
    mode = QuizModeFactory.create("sequential")
    assert isinstance(mode, SequentialMode)
    assert mode.order(cards, {}) == cards
    with pytest.raises(ValueError, match="Unknown quiz mode"):
        QuizModeFactory.create("invalid")


def test_random_shuffles_copy(
    cards: list[Flashcard], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Replace shuffling with reversal and check order and the first input card.

    Does not check real randomness, distribution, or every input element after
    the call; checking one card does not prove the entire input is unchanged.
    """

    def reverse(items: list[Flashcard]) -> None:
        items.reverse()

    monkeypatch.setattr("quiz_engine.random.shuffle", reverse)
    assert isinstance(QuizModeFactory.create("random"), RandomMode)
    assert RandomMode().order(cards, {}) == list(reversed(cards))
    assert cards[0]["front"] == "one"


def test_adaptive_prioritizes_misses(cards: list[Flashcard]) -> None:
    """Order cards by two different saved miss counts ahead of an unseen card.

    Does not check ties, duplicate cards, or updating history during ordering.
    """
    mode = QuizModeFactory.create("adaptive")
    assert isinstance(mode, AdaptiveMode)
    history = {card_key(cards[1]): 1, card_key(cards[2]): 2}
    assert mode.order(cards, history) == [cards[2], cards[1], cards[0]]


def test_answer_updates_stats_and_history(cards: list[Flashcard]) -> None:
    """Check answer normalization, scoring, miss recording, and miss clearing.

    Does not test persistence, all Unicode case variants, or the final accuracy
    after the third answer.
    """
    history: dict[str, int] = {}
    engine = QuizEngine(cards, SequentialMode(), history)
    assert engine.stats.accuracy == 0
    assert not engine.answer(cards[1], "wrong")
    assert engine.answer(cards[0], "  FIRST  ")
    assert engine.stats.total == 2
    assert engine.stats.accuracy == 50
    assert engine.stats.missed == ["two"]
    assert history == {card_key(cards[1]): 1}
    assert engine.answer(cards[1], "second")
    assert history == {}


def test_history_round_trip_and_deck_isolation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Save and reload history while isolating two distinct deck paths.

    Does not cover concurrent writers, identical cards, or path relocation.
    """
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    first = history_path(tmp_path / "first.json")
    second = history_path(tmp_path / "second.json")
    assert first != second
    assert load_history(first) == {}
    save_history(first, {"card": 2})
    assert load_history(first) == {"card": 2}
    assert load_history(second) == {}


def test_history_location_error_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Convert a simulated unavailable home directory into a HistoryError.

    Does not check other path-resolution failures or the full error message.
    """

    def fail_home() -> Path:
        raise RuntimeError("home directory unavailable")

    monkeypatch.setattr(Path, "home", fail_home)
    with pytest.raises(HistoryError, match="history location"):
        history_path(tmp_path / "deck.json")


@pytest.mark.parametrize("data", ["{", '{"card": true}', '{"card": 0}', "[]"])
def test_rejects_bad_history(tmp_path: Path, data: str) -> None:
    """Reject malformed JSON, boolean or zero counts, and a non-object history.

    Checks only the exception type, not its message or all invalid values.
    """
    path = tmp_path / "history.json"
    path.write_text(data, encoding="utf-8")
    with pytest.raises(HistoryError):
        load_history(path)


def test_reports_excessively_nested_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Convert a simulated history decoder RecursionError into a HistoryError.

    Does not exercise actual deeply nested JSON or determine the nesting limit.
    """
    path = tmp_path / "history.json"
    path.write_text("{}", encoding="utf-8")

    def reject_nesting(file: object) -> object:
        raise RecursionError("too deep")

    monkeypatch.setattr("utils.history.json.load", reject_nesting)
    with pytest.raises(HistoryError, match="nesting"):
        load_history(path)


def test_reports_history_write_failure(tmp_path: Path) -> None:
    """Report a save failure when the intended parent path is a regular file.

    Does not simulate other I/O failures or inspect temporary-file cleanup.
    """
    parent = tmp_path / "not_a_directory"
    parent.write_text("x", encoding="utf-8")
    with pytest.raises(HistoryError, match="Cannot save history"):
        save_history(parent / "history.json", {"key": 1})


def test_save_failure_preserves_existing_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Preserve existing saved history when the final file replacement fails.

    Simulates os.replace failure; it does not check temporary-file cleanup,
    crashes, concurrent writes, or failures at earlier write stages.
    """
    path = tmp_path / "history.json"
    save_history(path, {"key": 1})

    def fail_replace(source: object, destination: object) -> None:
        raise OSError("replace failed")

    monkeypatch.setattr("utils.history.os.replace", fail_replace)
    with pytest.raises(HistoryError, match="replace failed"):
        save_history(path, {"key": 2})
    assert json.loads(path.read_text(encoding="utf-8")) == {"key": 1}
