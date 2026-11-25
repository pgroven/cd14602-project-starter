"""Store diagnostic records in UTC-dated files with startup retention."""

import logging
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

LOG_NAME = re.compile(r"quiz-(\d{4}-\d{2}-\d{2})\.log\Z")


def prepare_log_directory(directory: Path, today: date) -> None:
    """Create the log directory and remove fully expired daily log files."""
    directory.mkdir(parents=True, exist_ok=True)
    cutoff = today - timedelta(days=30)
    for path in directory.iterdir():
        match = LOG_NAME.fullmatch(path.name)
        if match is None or path.is_symlink() or not path.is_file():
            continue
        try:
            log_date = date.fromisoformat(match.group(1))
        except ValueError:
            continue
        if log_date < cutoff:
            path.unlink()


class DailyLogHandler(logging.Handler):
    """Append records to UTC-dated files, warning once on a write failure."""

    def __init__(self, directory: Path) -> None:
        super().__init__()
        self.directory = directory
        self.failed = False
        formatter = logging.Formatter(
            "%(asctime)sZ %(levelname)s %(message)s", "%Y-%m-%dT%H:%M:%S"
        )
        formatter.converter = time.gmtime
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        if self.failed:
            return
        day = datetime.fromtimestamp(record.created, timezone.utc).date()
        path = self.directory / f"quiz-{day.isoformat()}.log"
        try:
            with path.open("a", encoding="utf-8") as log_file:
                log_file.write(self.format(record) + "\n")
        except (OSError, UnicodeError) as exc:
            self.failed = True
            message = f"Warning: Cannot write diagnostic log: {exc}"
            print(message, file=sys.stderr)
