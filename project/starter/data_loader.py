"""Load and validate flashcard decks."""

from pathlib import Path
from typing import TypedDict, Union

from utils.file_handler import FileReadError, read_json


class Flashcard(TypedDict):
    front: str
    back: str


class FlashcardLoadError(Exception):
    """A flashcard deck could not be loaded or validated."""


def load_flashcards(path: Union[str, Path]) -> list[Flashcard]:
    """Load a nonempty array of cards, optionally wrapped in a cards object."""
    try:
        data = read_json(path)
    except FileReadError as exc:
        raise FlashcardLoadError(str(exc)) from exc

    if isinstance(data, dict):
        if "cards" not in data:
            raise FlashcardLoadError("Deck must contain a 'cards' array.")
        data = data["cards"]
    if not isinstance(data, list):
        raise FlashcardLoadError("Deck must be an array of cards.")
    if not data:
        raise FlashcardLoadError("Deck must contain at least one card.")

    cards: list[Flashcard] = []
    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise FlashcardLoadError(f"Card {index} must be an object.")
        for field in ("front", "back"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                raise FlashcardLoadError(
                    f"Card {index} must have a nonempty string '{field}'."
                )
            try:
                value.encode("utf-8")
            except UnicodeEncodeError as exc:
                raise FlashcardLoadError(
                    f"Card {index} field '{field}' contains invalid Unicode."
                ) from exc
        cards.append(Flashcard(front=item["front"], back=item["back"]))
    return cards
