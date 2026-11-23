"""Persist unresolved misses separately for each deck."""

import hashlib
import json
import os
import tempfile
from pathlib import Path


class HistoryError(Exception):
    """Quiz history could not be read or saved."""


def history_path(deck_path: Path) -> Path:
    """Return a per-deck path under the current user's home directory."""
    try:
        resolved = str(deck_path.resolve()).encode("utf-8")
        deck_id = hashlib.sha256(resolved).hexdigest()
        return Path.home() / ".flashcard_quizzer" / f"{deck_id}.json"
    except (OSError, RuntimeError, UnicodeError) as exc:
        message = f"Cannot determine history location: {exc}"
        raise HistoryError(message) from exc


def load_history(path: Path) -> dict[str, int]:
    """Load history, refusing malformed or unreadable files."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data: object = json.load(file)
    except FileNotFoundError:
        return {}
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HistoryError(f"Cannot read history {path}: {exc}") from exc
    except RecursionError as exc:
        raise HistoryError(f"History nesting is too deep in {path}") from exc
    except ValueError as exc:
        raise HistoryError(f"Cannot read history {path}: {exc}") from exc

    if not isinstance(data, dict) or any(
        not isinstance(key, str)
        or not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
        for key, value in data.items()
    ):
        raise HistoryError(f"Invalid history in {path}: expected counts > 0")
    return data


def save_history(path: Path, history: dict[str, int]) -> None:
    """Atomically replace history so interrupted writes do not corrupt it."""
    temporary_path = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, delete=False
        ) as file:
            temporary_path = Path(file.name)
            json.dump(history, file, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, path)
        temporary_path = None
    except OSError as exc:
        raise HistoryError(f"Cannot save history {path}: {exc}") from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError as exc:
                raise HistoryError(
                    f"Cannot remove temporary history {temporary_path}: {exc}"
                ) from exc
