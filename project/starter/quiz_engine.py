"""Quiz ordering strategies, answer evaluation, and session statistics."""

import hashlib
import json
import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Mapping, Sequence

from data_loader import Flashcard


def card_key(card: Flashcard) -> str:
    """Identify a card by its front and back, independent of deck order."""
    content = json.dumps([card["front"], card["back"]], ensure_ascii=False)
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


class QuizMode(ABC):
    """Strategy for ordering a deck."""

    @abstractmethod
    def order(
        self, cards: Sequence[Flashcard], history: Mapping[str, int]
    ) -> list[Flashcard]:
        """Return the cards in the order they should be presented."""


class SequentialMode(QuizMode):
    def order(
        self, cards: Sequence[Flashcard], history: Mapping[str, int]
    ) -> list[Flashcard]:
        return list(cards)


class RandomMode(QuizMode):
    def order(
        self, cards: Sequence[Flashcard], history: Mapping[str, int]
    ) -> list[Flashcard]:
        shuffled = list(cards)
        random.shuffle(shuffled)
        return shuffled


class AdaptiveMode(QuizMode):
    def order(
        self, cards: Sequence[Flashcard], history: Mapping[str, int]
    ) -> list[Flashcard]:
        return sorted(cards, key=lambda card: -history.get(card_key(card), 0))


class QuizModeFactory:
    """Create a quiz ordering strategy from a mode name."""

    @staticmethod
    def create(name: str) -> QuizMode:
        modes: dict[str, type[QuizMode]] = {
            "sequential": SequentialMode,
            "random": RandomMode,
            "adaptive": AdaptiveMode,
        }
        try:
            mode = modes[name]
        except KeyError as exc:
            raise ValueError(f"Unknown quiz mode: {name}") from exc
        return mode()


@dataclass
class SessionStats:
    total: int = 0
    correct: int = 0
    missed: list[str] = field(default_factory=list)

    @property
    def accuracy(self) -> float:
        return 100.0 * self.correct / self.total if self.total else 0.0


class QuizEngine:
    """Track results and unresolved misses for an ordered quiz."""

    def __init__(
        self,
        cards: Sequence[Flashcard],
        mode: QuizMode,
        history: dict[str, int],
    ) -> None:
        self.cards = mode.order(cards, history)
        self.history = history
        self.stats = SessionStats()

    def answer(self, card: Flashcard, answer: str) -> bool:
        """Record an answer and update the card's unresolved miss count."""
        correct = answer.strip().casefold() == card["back"].strip().casefold()
        self.stats.total += 1
        key = card_key(card)
        if correct:
            self.stats.correct += 1
            self.history.pop(key, None)
        else:
            self.stats.missed.append(card["front"])
            self.history[key] = self.history.get(key, 0) + 1
        return correct
