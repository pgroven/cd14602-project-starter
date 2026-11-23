"""Entry point for the Flashcard Quizzer CLI."""

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from data_loader import FlashcardLoadError, load_flashcards
from quiz_engine import QuizEngine, QuizModeFactory
from ui import run_quiz, show_history
from utils.history import HistoryError, history_path, load_history


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Run a quiz and return a process exit code."""
    parser = argparse.ArgumentParser(description="Flashcard quiz.")
    parser.add_argument("-f", "--file", required=True, help="Path to a deck")
    parser.add_argument(
        "-m",
        "--mode",
        choices=("sequential", "random", "adaptive"),
        default="sequential",
        help="Card ordering mode (default: sequential)",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Show saved misses before quiz"
    )
    args = parser.parse_args(argv)
    try:
        cards = load_flashcards(args.file)
        path = history_path(Path(args.file))
        history = load_history(path)
        if args.stats:
            show_history(cards, history)
        engine = QuizEngine(cards, QuizModeFactory.create(args.mode), history)
        run_quiz(engine, path)
    except (FlashcardLoadError, HistoryError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nQuiz interrupted; the latest answer may not have been saved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
