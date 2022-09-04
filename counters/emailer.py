"""emailer.py

Handles emailing myself details of failure.

Official documentation for simple examples with Python stdlib:
https://docs.python.org/3/library/email.examples.html
"""

import smtplib
from dataclasses import dataclass, field
from datetime import date
from email.message import EmailMessage

from .config import DATE_FORMAT, ERROR_EMAIL


@dataclass
class TaskFailure:
    """Object to compile raised exceptions in."""

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


def _format_content(fails: TaskFailure) -> str:
    # TODO
    return ""


def send_email(fails: TaskFailure) -> None:
    content = _format_content(fails)

    # Construct email object
    message = EmailMessage()
    message.set_content(content)
    message["Subject"] = f"Error in counters program {date.today()}"
    message["From"] = ERROR_EMAIL
    message["To"] = ERROR_EMAIL

    # Send email to self through localhost
    smtp = smtplib.SMTP("localhost")
    smtp.send_message(message)
    smtp.quit()
