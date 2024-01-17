"""writer.py

Logs the extracted status to the destination file.
"""

import csv
import os
from datetime import datetime

from . import ensure_file_path

DESTINATION_PATH = os.path.join(os.path.expanduser("~"),
                                ".config/status-logger/statuses.csv")


def log_status(emoji: str | None, text: str) -> None:
    """Log the status to the CSV file.

    Args:
        emoji (str | None): The emoji part of the status as a Unicode
        character. None if the status did not use an emoji.
        text (str): The text part of the status.

    Postcondition:
        The CSV file exists at the destination path.
    """
    ensure_file_path(DESTINATION_PATH)

    # Ideally, I'll have a status per day, so the date should be enough
    # The time part is included for potential debugging purposes
    timestamp = datetime.now()
    date = timestamp.date()
    time = timestamp.time()

    # According to: https://docs.python.org/3/library/csv.html#csv.writer
    # File objects should use newline=""
    # encoding kwarg is necessary because emojis are Unicode chars
    with open(DESTINATION_PATH, "at", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        writer.writerow([date, time, emoji, text])
