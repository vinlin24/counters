"""__main__.py

Entry point.
"""

import sys
from datetime import date

from . import parse_args, run_program
from .dry_run import print_dry_run
from .emailer import send_email
from .logger import TaskFailure, format_content, log_report, logging

# Parse and unpack debugging options
ns = parse_args()
console_only: bool = ns.console
windowed: bool = ns.window
d: bool = ns.discord
i: bool = ns.instagram
s: bool = ns.spotify
g: bool = ns.github
dry_run_date: date | None = ns.dry_run

if console_only:
    logging.disable(100)

if dry_run_date is not None:
    print_dry_run(dry_run_date)
    sys.exit(0)

# Run program
fails = TaskFailure()
run_program(fails, windowed, d, i, s, g)

# Log and send failure report is there was any error
if not console_only:
    report = format_content(fails, d, i, s, g)
    log_report(report)
    send_email(report)
else:
    fails.print_tracebacks()
