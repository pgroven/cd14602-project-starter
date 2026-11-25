"""Entry point for the Flashcard Quizzer CLI."""

import argparse
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Sequence

from data_loader import FlashcardLoadError, load_flashcards
from quiz_engine import QuizEngine, QuizModeFactory
from ui import run_quiz, show_history
from utils.diagnostic_logging import DailyLogHandler, prepare_log_directory
from utils.history import HistoryError, history_path, load_history

logger = logging.getLogger("flashcard_quizzer")


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
    parser.add_argument(
        "--verbose", action="store_true", help="Show debug details and traces"
    )
    args = parser.parse_args(argv)
    try:
        log_directory = Path.home() / ".flashcard_quizzer" / "logs"
        prepare_log_directory(log_directory, datetime.now(timezone.utc).date())
    except (OSError, RuntimeError) as exc:
        print(f"Error: Cannot prepare diagnostic logs: {exc}", file=sys.stderr)
        return 1
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(message)s"))
    file_handler = DailyLogHandler(log_directory)
    previous_level = logger.level
    previous_propagate = logger.propagate
    logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)
    logger.propagate = False
    logger.addHandler(handler)
    logger.addHandler(file_handler)
    try:
        logger.info("Loading deck: %s", Path(args.file).absolute())
        logger.debug("Debug: selected quiz mode: %s", args.mode)
        cards = load_flashcards(args.file)
        logger.debug("Debug: loaded %d cards", len(cards))
        path = history_path(Path(args.file))
        logger.info("Loading history: %s", path)
        history = load_history(path)
        logger.debug("Debug: loaded %d missed-card records", len(history))
        if args.stats:
            show_history(cards, history)
        engine = QuizEngine(cards, QuizModeFactory.create(args.mode), history)
        run_quiz(engine, path)
        logger.debug("Debug: answered %d questions", engine.stats.total)
    except (FlashcardLoadError, HistoryError) as exc:
        logger.error("Error: %s", exc, exc_info=args.verbose)
        return 1
    except Exception as exc:
        logger.error(
            "Error: Unexpected %s: %s",
            type(exc).__name__,
            exc,
            exc_info=args.verbose,
        )
        return 1
    except KeyboardInterrupt:
        print("\nQuiz interrupted; the latest answer may not have been saved.")
    finally:
        logger.removeHandler(handler)
        handler.close()
        logger.removeHandler(file_handler)
        file_handler.close()
        logger.setLevel(previous_level)
        logger.propagate = previous_propagate
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
