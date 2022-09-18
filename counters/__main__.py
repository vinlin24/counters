"""__main__.py

Entry point.
"""

import sys
from argparse import ArgumentParser

from . import run_program
from .emailer import send_email
from .logger import TaskFailure, format_content, log_report

parser = ArgumentParser(description="Manually run counters program")
"""Simple command line parser for debugging."""

# Output to console only, don't touch log file and don't email
parser.add_argument("-c", "--console", action="store_true")
# Run with a browser window instead of headlessly
parser.add_argument("-w", "--window", action="store_true")
# If any of these are included, run those select tasks instead of all
parser.add_argument("-d", "--discord", action="store_true")
parser.add_argument("-i", "--instagram", action="store_true")
parser.add_argument("-s", "--spotify", action="store_true")
ns = parser.parse_args(sys.argv[1:])

# Unpack arguments
console_only: bool = ns.console
windowed: bool = ns.window
d: bool = ns.discord
i: bool = ns.instagram
s: bool = ns.spotify

# If no flags were supplied, run all as default behavior
# This way it doesn't break the task set up in Task Scheduler
if not any((d, i, s)):
    d = i = s = True

# Run program
fails = TaskFailure()
run_program(fails, windowed, d, i, s)

report = format_content(fails, d, i, s)

# Log and send failure report is there was any error
if not console_only:
    log_report(report)
    send_email(report)
