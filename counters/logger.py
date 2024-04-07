"""logger.py

Handles logging the status of the run to the dedicated log file.
"""

import logging
import os
import re
import traceback
from datetime import datetime
from pathlib import Path
from typing import Generator

from .config import (EXIT_FAILURE_GITHUB, EXIT_FAILURE_INSTAGRAM,
                     EXIT_FAILURE_SPOTIFY, LOG_FILE_PATH, PLATFORM_GITHUB,
                     PLATFORM_INSTAGRAM, PLATFORM_SPOTIFY)
from .utils import print_error

logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode="at",
                    encoding="utf-8",
                    level=logging.INFO,
                    format="[%(asctime)s] %(message)s")
log = logging.getLogger(__package__)


class FailureLog:
    """Object to record exceptions raised in main process."""

    def __init__(self) -> None:
        self.json: Exception | None = None
        """Error in loading the central JSON file."""

        self.driver: Exception | None = None
        """Error in loading the Edge web driver."""

        self.platforms: dict[str, Exception] = {}
        """Error in updating the platforms."""

    def all_good(self) -> bool:
        """Return whether no failures were set."""
        return self.json is None and self.driver is None and not self.platforms

    def print_tracebacks(self) -> None:
        """Print the stored tracebacks for --console debugging."""
        if self.json:
            print_error(self._format_error(self.json))
        if self.driver:
            print_error(self._format_error(self.driver))
        for exc in self.platforms.values():
            print_error(self._format_error(exc))

    def get_exit_code(self) -> int:
        """
        Return the exit code encoding the success/failure(s) of the
        tasks.
        """
        result = 0

        if PLATFORM_GITHUB in self.platforms:
            result |= EXIT_FAILURE_GITHUB
        if PLATFORM_INSTAGRAM in self.platforms:
            result |= EXIT_FAILURE_INSTAGRAM
        if PLATFORM_GITHUB in self.platforms:
            result |= EXIT_FAILURE_GITHUB

        # Spotify is by playlist, so the "platform" names mention
        # playlist ID instead of just "Spotify".
        if any(PLATFORM_SPOTIFY in key for key in self.platforms.keys()):
            result |= EXIT_FAILURE_SPOTIFY

        return result

    def generate_report(self, platforms_attempted: list[str]) -> str | None:
        """Generate the status report from stored exceptions.

        Args:
            platforms_attempted (list[str]): The `.platform_name`s of
            the updaters executed.

        Returns:
            str | None: Text to log or send. Return None if there are no
            errors i.e. `failure_log.all_good() is True`.
        """
        if self.all_good():
            return None

        # Check the setup ones in the order they would be set.
        if self.json:
            content = "There was an error loading the central JSON file:\n"
            content += self._format_error(self.json)
            # No other errors could be reached if this failed.
            return content
        if self.driver:
            content = "There was an error initializing the Edge web driver:\n"
            content += self._format_error(self.driver)
            # No other errors could be reached if this failed.
            return content

        # Summary lines.
        summaries = list[str]()

        # Independent task failures.
        content = ""

        for platform_name in platforms_attempted:
            exc = self.platforms.get(platform_name)
            if exc is None:
                summaries.append(f"{platform_name}: SUCCESS")
            else:
                content += f"Couldn't update {platform_name}:\n"
                content += self._format_error(exc)
                summaries.append(f"{platform_name}: FAILED")

        content += "\n".join(summaries) + "\n"

        # Disclaimer.
        repo_path = Path(__file__).parent.parent  # file -> package -> repo
        content += (
            "\nThis message was automatically generated and sent by the "
            f"counters program running locally at {repo_path}.\n"
        )

        return content

    def write_report_to_file(self, report: str | None) -> None:
        """Log the status of the program's execution.

        Args:
            report (str | None): Error report. None if no errors
            occurred.
        """
        entry = f"[{datetime.now()}] "
        if report is None:
            entry += "No problems detected.\n"
        else:
            entry += f"Encountered errors:\n{report}\n"

        with LOG_FILE_PATH.open("at", encoding="utf-8") as fp:
            fp.write(entry)

    def _format_error(self, error: Exception) -> str:
        """Return the traceback of the error as a string.

        Postcondition:
            Adds an extra newline for padding.
        """
        return "".join(traceback.format_exception(error)) + "\n"


def get_last_success_timestamp() -> datetime | None:
    """
    Parse the log file for the most recent "No problems detected." entry
    and return the timestamp at which it was logged. Return None if no
    such entry could be found.
    """
    matcher = re.compile(r"\[(.+?)\] No problems detected.")
    for line in _reverse_readline(LOG_FILE_PATH):
        match = matcher.match(line)
        if match is not None:
            timestamp: str = match.group(1)
            return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    return None


def _reverse_readline(
    file_path: Path,
    buf_size: int = 8192
) -> Generator[str, None, None]:
    """Yield the lines of a file in reverse order.

    Code adapted from: https://stackoverflow.com/a/23646049/14226122.
    """
    with file_path.open("rb") as fp:
        segment = None
        offset = 0
        fp.seek(0, os.SEEK_END)
        file_size = remaining_size = fp.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fp.seek(file_size - offset)
            buffer = fp.read(
                min(remaining_size, buf_size)).decode(
                encoding="utf-8")
            remaining_size -= buf_size
            lines = buffer.split("\n")
            # The first line of the buffer is probably not a complete
            # line so we'll save it and append it to the last line of
            # the next buffer we read.
            if segment is not None:
                # If the previous chunk starts right from the beginning
                # of line do not concat the segment to the last line of
                # new chunk. Instead, yield the segment first.
                if buffer[-1] != "\n":
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    yield lines[index]
        # Don't yield None if the file was empty.
        if segment is not None:
            yield segment
