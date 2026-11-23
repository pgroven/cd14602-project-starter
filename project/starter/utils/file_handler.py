"""Read JSON files with actionable errors."""

import json
from pathlib import Path
from typing import Union


class FileReadError(Exception):
    """A JSON file could not be read."""


def read_json(path: Union[str, Path]) -> object:
    """Read a UTF-8 JSON file, reporting file and parsing errors."""
    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as exc:
        raise FileReadError(f"File not found: {file_path}") from exc
    except UnicodeDecodeError as exc:
        raise FileReadError(f"File is not valid UTF-8: {file_path}") from exc
    except json.JSONDecodeError as exc:
        raise FileReadError(
            f"Invalid JSON in {file_path} at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc
    except RecursionError as exc:
        raise FileReadError(f"JSON nesting too deep in {file_path}") from exc
    except ValueError as exc:
        raise FileReadError(f"Cannot read JSON in {file_path}: {exc}") from exc
    except OSError as exc:
        message = f"Cannot read {file_path}: {exc.strerror or exc}"
        raise FileReadError(message) from exc
