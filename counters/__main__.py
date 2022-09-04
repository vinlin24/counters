"""__main__.py

Entry point.
"""

from . import run_program
from .emailer import TaskFailure, send_email

# Run program
fails = TaskFailure()
run_program(fails)

# Send failure report is there was any error:
if not fails.all_good():
    send_email(fails)
