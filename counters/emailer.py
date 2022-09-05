"""emailer.py

Handles emailing myself details of failure.

Official documentation for simple examples with Python stdlib:
https://docs.python.org/3/library/email.examples.html
"""

import smtplib
from datetime import date
from email.message import EmailMessage

from .config import ERROR_EMAIL, ERROR_EMAIL_PASSWORD


def send_email(content: str | None) -> None:
    """Send an email to myself with an error report if errors occurred.

    Args:
        content (str | None): Text to send as the body of the email.
        None if there's nothing to send (no errors occurred).

    Postcondition:
        Does nothing if param content is None.
    """
    if content is None:
        print("No failures recorded, not sending email.")
        return

    print("Failures recorded, sending email...")

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
