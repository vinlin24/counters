"""emailer.py

Handles emailing myself details of failure.

Official documentation for simple examples with Python stdlib:
https://docs.python.org/3/library/email.examples.html
"""

import smtplib
import traceback
from dataclasses import dataclass, field
from datetime import date
from email.message import EmailMessage
from pathlib import Path

from .config import ERROR_EMAIL, ERROR_EMAIL_PASSWORD


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


def _format_content(fails: TaskFailure) -> str:
    """Generate the body of the email to send from stored exceptions.

    Args:
        fails (TaskFailure): Exception recorder instance.

    Returns:
        str: Body of the email to send.

    Postcondition:
        Not that any function gives a shit after this but
        `fails.spotify[None]`, if exists, is popped. 
    """
    # Check the setup ones in the order they would be set
    if fails.json:
        content = "There was an error loading the central JSON file:\n"
        content += _format_error(fails.json)
        return content  # No other errors could be reached if this failed
    if fails.driver:
        content = "There was an error initializing the Edge web driver:\n"
        content += _format_error(fails.driver)
        return content  # No other errors could be reached if this failed

    # Independent task failures
    content = ""
    if fails.discord:
        content += "Couldn't update Discord custom status:\n"
        content += _format_error(fails.discord)
    if fails.instagram:
        content += "Couldn't update Instagram custom status:\n"
        content += _format_error(fails.instagram)

    if fails.spotify:
        if None in fails.spotify:
            content += "There was an error getting the Spotify tasks:\n"
            content += _format_error(fails.spotify[None])
        else:
            for playlist_id, error in fails.spotify.items():
                content += ("Couldn't update details of Spotify playlist with "
                            f"ID {playlist_id}:\n")
                content += _format_error(error)

    # Summary
    d = "Discord: " + ("FAILED" if fails.discord else "SUCCESS")
    i = "Instagram: " + ("FAILED" if fails.instagram else "SUCCESS")
    summaries = [d, i]
    if fails.spotify:
        # Ignore None case for playlist summary
        fails.spotify.pop(None, None)
        for playlist_id in fails.spotify.keys():
            s = f"Spotify (ID={playlist_id}): " + \
                ("FAILED" if fails.spotify else "SUCCESS")
            summaries.append(s)
    else:
        summaries.append("Spotify: SUCCESS")
    content += "\n".join(summaries) + "\n"

    # Disclaimer
    repo_path = Path(__file__).parent.parent  # file -> package -> repo
    content += ("\nThis message was automatically generated and sent by the "
                f"counters program running locally at {repo_path}.\n")

    return content


def send_email(fails: TaskFailure) -> None:
    """Send an email to myself with an error report if errors occurred.

    Args:
        fails (TaskFailure): Dataclass recording the exception
        instances raised by the program.

    Postcondition:
        Does nothing if there were no errors raised i.e. if
        `fails.all_good()` returns True.
    """
    if fails.all_good():
        print("No failures recorded.")
        return

    print("Failures recorded, sending email...")
    content = _format_content(fails)

    # Construct email object
    message = EmailMessage()
    message.set_content(content)
    message["Subject"] = f"Error in counters program {date.today()}"
    message["From"] = ERROR_EMAIL
    message["To"] = ERROR_EMAIL

    # Send email to self through Outlook server
    # https://www.arclab.com/en/kb/email/list-of-smtp-and-imap-servers-mailserver-list.html
    host, port = "smtp-mail.outlook.com", 587
    with smtplib.SMTP(host, port) as smtp:
        smtp.starttls()
        smtp.login(user=ERROR_EMAIL, password=ERROR_EMAIL_PASSWORD)
        smtp.send_message(message)

    print("Email sent successfully.")
