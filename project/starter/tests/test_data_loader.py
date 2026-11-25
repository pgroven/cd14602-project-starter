"""Tests for flashcard loading and the validation CLI."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, NoReturn, Optional

import pytest

from data_loader import FlashcardLoadError, load_flashcards
from main import main

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("filename", ["glossary.json", "python_basics.json"])
def test_loads_both_sample_formats(filename: str) -> None:
    """Load each sample format and verify the returned cards are nonempty.

    Does not check exact card contents, counts, or ordering.
    """
    cards = load_flashcards(ROOT / "data" / filename)
    assert cards
    assert all(card["front"] and card["back"] for card in cards)


@pytest.mark.parametrize(
    ("data", "message"),
    [
        ({}, "'cards'"),
        ({"cards": None}, "array"),
        ("not an array", "array"),
        ([], "at least one"),
        ([None], "Card 1"),
        ([{"front": "question"}], "'back'"),
        ([{"back": "answer"}], "'front'"),
        ([{"front": " ", "back": "answer"}], "'front'"),
        ([{"front": "question", "back": 42}], "'back'"),
    ],
)
def test_rejects_invalid_deck(tmp_path: Path, data: Any, message: str) -> None:
    """Reject the parameterized invalid deck structures and card fields.

    Checks the exception and a message fragment, not every invalid structure
    or the complete error message.
    """
    path = tmp_path / "deck.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(FlashcardLoadError, match=message):
        load_flashcards(path)


def test_reports_missing_file(tmp_path: Path) -> None:
    """Report a nonexistent deck as a FlashcardLoadError.

    Does not check permissions or the CLI's printed message.
    """
    with pytest.raises(FlashcardLoadError, match="File not found"):
        load_flashcards(tmp_path / "missing.json")


def test_reports_deck_read_permission_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Check a denied deck read reports the path, read access, and directories.

    Exercises the loader and CLI with a simulated permission error. Does not
    inspect filesystem permissions or assert the exact directory permission.
    """
    path = tmp_path / "deck.json"
    content = '[{"front": "question", "back": "answer"}]'
    path.write_text(content, encoding="utf-8")

    def deny_open(self: Path, *args: object, **kwargs: object) -> NoReturn:
        raise PermissionError("access denied")

    monkeypatch.setattr(Path, "open", deny_open)
    with pytest.raises(FlashcardLoadError) as error:
        load_flashcards(path)
    assert str(path) in str(error.value)
    assert "read permission" in str(error.value)
    assert "parent directories" in str(error.value)

    assert main(["--file", str(path)]) == 1
    stderr = capsys.readouterr().err
    assert str(path) in stderr
    assert "read permission" in stderr
    assert "parent directories" in stderr
    assert "Traceback" not in stderr


def test_reports_directory_instead_of_file(tmp_path: Path) -> None:
    """Report a directory supplied as a deck instead of opening it.

    Does not check other file access failures or the full error message.
    """
    with pytest.raises(FlashcardLoadError, match="Cannot read"):
        load_flashcards(tmp_path)


@pytest.mark.parametrize(
    ("content", "message"),
    [(b'{"cards": [}', "Invalid JSON"), (b"\xff", "valid UTF-8")],
)
def test_reports_unreadable_content(
    tmp_path: Path, content: bytes, message: str
) -> None:
    """Reject malformed JSON and invalid UTF-8 bytes with relevant messages.

    Does not cover every JSON parsing or encoding error.
    """
    path = tmp_path / "deck.json"
    path.write_bytes(content)
    with pytest.raises(FlashcardLoadError, match=message):
        load_flashcards(path)


@pytest.mark.parametrize("field", ["front", "back"])
def test_cli_rejects_unpaired_surrogate(tmp_path: Path, field: str) -> None:
    """Reject an unpaired surrogate in either card field through the CLI.

    Checks nonzero exit, field identification, and no traceback; it does not
    check every invalid Unicode sequence or the complete error message.
    """
    card = {"front": "question", "back": "answer"}
    card[field] = "\ud800"
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps([card]), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), "-f", str(path)],
        capture_output=True,
        text=True,
        input="exit\n",
        check=False,
    )
    assert result.returncode != 0
    assert "Card 1" in result.stderr and f"'{field}'" in result.stderr
    assert "Traceback" not in result.stderr


def test_reports_excessively_nested_json(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Convert a simulated JSON decoder RecursionError into a loader error.

    Does not determine the actual nesting limit or exercise deeply nested JSON.
    """
    path = tmp_path / "nested.json"
    path.write_text("[]", encoding="utf-8")

    def reject_nesting(file: object) -> object:
        raise RecursionError("too deep")

    monkeypatch.setattr("utils.file_handler.json.load", reject_nesting)
    with pytest.raises(FlashcardLoadError, match="nesting"):
        load_flashcards(path)


def test_loads_valid_unicode_card(tmp_path: Path) -> None:
    """Decode a valid escaped surrogate pair in a card's front field.

    Does not check other Unicode characters or the returned back field.
    """
    path = tmp_path / "unicode.json"
    data = '[{"front": "\\ud83d\\ude00", "back": "smile"}]'
    path.write_text(data, encoding="utf-8")
    assert load_flashcards(path)[0]["front"] == "\U0001f600"


@pytest.mark.parametrize(
    ("content", "message"),
    [
        (None, "File not found"),
        ("{", "Invalid JSON"),
        ('[{"front": "q"}]', "'back'"),
    ],
)
def test_cli_reports_errors_without_traceback(
    tmp_path: Path, content: Optional[str], message: str
) -> None:
    """Check CLI errors for missing, malformed, and incomplete deck files.

    Requires a nonzero exit, relevant stderr fragment, and no traceback; it
    does not check exact exit codes, stdout, or every invalid deck.
    """
    path = tmp_path / "bad.json"
    if content is not None:
        path.write_text(content, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "main.py"), "--file", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert message in result.stderr
    assert "Traceback" not in result.stderr


def test_cli_loads_deck() -> None:
    """Load the glossary in a subprocess and exit before answering a card.

    Checks the first prompt and zero-question summary, not a completed quiz,
    other deck formats, or the full summary.
    """
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "main.py"),
            "-f",
            str(ROOT / "data" / "glossary.json"),
        ],
        capture_output=True,
        text=True,
        input="exit\n",
        check=False,
    )
    assert result.returncode == 0
    assert "API" in result.stdout
    assert "Total Questions | 0" in result.stdout
