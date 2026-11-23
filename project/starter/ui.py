"""Terminal interaction for the flashcard quiz."""

import os
import sys
from pathlib import Path
from typing import Mapping, Sequence

from data_loader import Flashcard
from quiz_engine import QuizEngine, SessionStats, card_key
from utils.history import save_history


def show_history(
    cards: Sequence[Flashcard],
    history: Mapping[str, int],
) -> None:
    """Display unresolved misses for cards in the current deck."""
    print("Previously missed cards:")
    missed = [card for card in cards if history.get(card_key(card), 0)]
    if not missed:
        print("  None")
    for card in missed:
        print(f"  {card['front']}: {history[card_key(card)]} missed")


def show_feedback(correct: bool, answer: str) -> None:
    """Print feedback, using terminal colors when supported."""
    message = "Correct!" if correct else f"Incorrect. Answer: {answer}"
    if sys.stdout.isatty() and "NO_COLOR" not in os.environ:
        color = "\033[32m" if correct else "\033[31m"
        message = f"{color}{message}\033[0m"
    print(message)


def show_summary(stats: SessionStats) -> None:
    """Print session statistics, including unanswered early exits."""
    print("\nSession summary")
    print(f"Total Questions | {stats.total}")
    print(f"Accuracy %      | {stats.accuracy:.1f}%")
    print("Missed terms    | " + (", ".join(stats.missed) or "None"))


def run_quiz(engine: QuizEngine, history_file: Path) -> None:
    """Run the interactive quiz and save each completed answer."""
    print("Type 'exit' to end the quiz.")
    for card in engine.cards:
        print(f"\n{card['front']}")
        while True:
            try:
                answer = input("Answer: ")
            except (KeyboardInterrupt, EOFError):
                print("\nQuiz ended.")
                show_summary(engine.stats)
                return
            if answer.strip():
                break
            print("Answer cannot be empty. Please try again.")
        if answer.strip().casefold() == "exit":
            print("Quiz ended.")
            break
        correct = engine.answer(card, answer)
        show_feedback(correct, card["back"])
        save_history(history_file, engine.history)
    show_summary(engine.stats)
