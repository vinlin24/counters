"""__main__.py

Entry point.
"""

from . import parse_args, run_program
from .emailer import send_email
from .logger import TaskFailure, format_content, log_report

# Parse and unpack debugging options
ns = parse_args()
console_only: bool = ns.console
windowed: bool = ns.window
d: bool = ns.discord
i: bool = ns.instagram
s: bool = ns.spotify

# Run program
fails = TaskFailure()
run_program(fails, windowed, d, i, s)

# Log and send failure report is there was any error
if not console_only:
    report = format_content(fails, d, i, s)
    log_report(report)
    send_email(report)
