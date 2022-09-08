"""logger.py

Handles logging the status of the run to the dedicated log file.
"""

import traceback
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .config import LOG_FILE_PATH


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

    def all_good(self) -> bool:
        """Return whether no failures were set."""
        return all(not val for val in self.__dict__.values())


def _format_error(error: Exception) -> str:
    """Return the traceback of the error as a string.

    Postcondition:
        Adds an extra newline for padding.
    """
    return "".join(traceback.format_exception(error)) + "\n"


def format_content(fails: TaskFailure,
                   discord: bool,
                   instagram: bool,
                   spotify: bool) -> str | None:
    """Generate the status report from stored exceptions.

    Args:
        fails (TaskFailure): Exception recorder instance.
        discord (bool): Whether the Discord task was run.
        instagram (bool): Whether the Instagram task was run.
        spotify (bool): Whether the Spotify tasks were run.

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

    with open(LOG_FILE_PATH, "at") as fp:
        fp.write(entry)
