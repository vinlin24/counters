"""__main__.py

Entry point.
"""

from . import run_program
from .emailer import send_email
from .logger import TaskFailure, format_content, log_report

# Run program
fails = TaskFailure()
run_program(fails)

report = format_content(fails)

# Log and send failure report is there was any error
log_report(report)
send_email(report)
