"""logger.py

Handles logging the status of the run to the dedicated log file.
"""

import logging
import os
import re
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Generator

from .config import (EXIT_FAILURE_GITHUB, EXIT_FAILURE_INSTAGRAM,
                     EXIT_FAILURE_SPOTIFY, LOG_FILE_PATH)

logging.basicConfig(filename=LOG_FILE_PATH,
                    filemode="at",
                    encoding="utf-8",
                    level=logging.INFO,
                    format="[%(asctime)s] %(message)s")
log = logging.getLogger(__package__)


@dataclass
class TaskFailure:
    """Object to record exceptions raised in main process."""

    json: Exception | None = None
    """Error in loading the central JSON file."""

    driver: Exception | None = None
    """Error in loading the Edge web driver."""

    discord: Exception | None = None
    """Error in the Discord task."""

    instagram: Exception | None = None
    """Error in the Instagram task."""

    spotify: dict[str | None, Exception] = \
        field(default_factory=dict)
    """Mapping of Spotify playlist ID to the error in its task.

    The key None is used for an error in getting the Spotify tasks
    itself and not in running the task for the playlist.
    """

    github: Exception | None = None
    """Error in the GitHub task."""

    def all_good(self) -> bool:
        """Return whether no failures were set."""
        return all(not val for val in self.__dict__.values())

    def print_tracebacks(self) -> None:
        """Print the stored tracebacks for --console debugging."""
        for val in self.__dict__.values():
            # self.spotify is a dict
            if val is self.spotify:
                for error in self.spotify.values():
                    print(_format_error(error))
            elif val:
                print(_format_error(val))

    def get_exit_code(self) -> int:
        """
        Return the exit code encoding the success/failure(s) of the
        tasks.
        """
        result = 0
        if self.github:
            result |= EXIT_FAILURE_GITHUB
        if self.instagram:
            result |= EXIT_FAILURE_INSTAGRAM
        if self.spotify:
            result |= EXIT_FAILURE_SPOTIFY
        if self.github:
            result |= EXIT_FAILURE_GITHUB
        return result


def _format_error(error: Exception) -> str:
    """Return the traceback of the error as a string.

    Postcondition:
        Adds an extra newline for padding.
    """
    return "".join(traceback.format_exception(error)) + "\n"


def format_content(fails: TaskFailure,
                   discord: bool,
                   instagram: bool,
                   spotify: bool,
                   github: bool,
                   ) -> str | None:
    """Generate the status report from stored exceptions.

    Args:
        fails (TaskFailure): Exception recorder instance.
        discord (bool): Whether the Discord task was run.
        instagram (bool): Whether the Instagram task was run.
        spotify (bool): Whether the Spotify tasks were run.
        github (bool): Whether the GitHub tasks were run.

    Returns:
        str | None: Text to log or send. Return None if there are no
        errors i.e. `fails.all_good() is True`.

    Postcondition:
        Not that any function gives a shit after this but
        `fails.spotify[None]`, if exists, is popped.
    """
    if fails.all_good():
        return None

    # Check the setup ones in the order they would be set
    if fails.json:
        content = "There was an error loading the central JSON file:\n"
        content += _format_error(fails.json)
        return content  # No other errors could be reached if this failed
    if fails.driver:
        content = "There was an error initializing the Edge web driver:\n"
        content += _format_error(fails.driver)
        return content  # No other errors could be reached if this failed

    # Summary lines
    summaries = []

    # Independent task failures
    content = ""
    if discord:
        if fails.discord:
            content += "Couldn't update Discord custom status:\n"
            content += _format_error(fails.discord)
            summaries.append("Discord: FAILED")
        else:
            summaries.append("Discord: SUCCESS")

    if instagram:
        if fails.instagram:
            content += "Couldn't update Instagram custom status:\n"
            content += _format_error(fails.instagram)
            summaries.append("Instagram: FAILED")
        else:
            summaries.append("Instagram: SUCCESS")

    if spotify:
        if fails.spotify:
            # Overall failure
            if None in fails.spotify:
                content += "There was an error getting the Spotify tasks:\n"
                content += _format_error(fails.spotify[None])
                summaries.append("Spotify: FAILED")
            # Playlist-specific failure
            else:
                for playlist_id, error in fails.spotify.items():
                    content += ("Couldn't update details of Spotify playlist with "
                                f"ID {playlist_id}:\n")
                    content += _format_error(error)
                    summaries.append(f"Spotify (ID={playlist_id}): FAILED")
        else:
            summaries.append("Spotify: SUCCESS")

    if github:
        if fails.github:
            content += "Couldn't update GitHub profile bio:\n"
            content += _format_error(fails.github)
            summaries.append("GitHub: FAILED")
        else:
            summaries.append("GitHub: SUCCESS")

    content += "\n".join(summaries) + "\n"

    # Disclaimer
    repo_path = Path(__file__).parent.parent  # file -> package -> repo
    content += ("\nThis message was automatically generated and sent by the "
                f"counters program running locally at {repo_path}.\n")

    return content


def log_report(report: str | None) -> None:
    """Log the status of the program's execution.

    Args:
        report (str | None): Error report. None if no errors occurred.
    """
    entry = f"[{datetime.now()}] "
    if report is None:
        entry += "No problems detected.\n"
    else:
        entry += f"Encountered errors:\n{report}\n"

    with open(LOG_FILE_PATH, "at", encoding="utf-8") as fp:
        fp.write(entry)


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
    filename: str | Path,
    buf_size: int = 8192
) -> Generator[str, None, None]:
    """Yield the lines of a file in reverse order.

    Code from: https://stackoverflow.com/a/23646049/14226122.
    """
    with open(filename, "rb") as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(
                min(remaining_size, buf_size)).decode(
                encoding="utf-8")
            remaining_size -= buf_size
            lines = buffer.split("\n")
            # The first line of the buffer is probably not a complete
            # line so we'll save it and append it to the last line of
            # the next buffer we read
            if segment is not None:
                # If the previous chunk starts right from the beginning
                # of line do not concat the segment to the last line of
                # new chunk. Instead, yield the segment first
                if buffer[-1] != "\n":
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                if lines[index]:
                    yield lines[index]
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment
