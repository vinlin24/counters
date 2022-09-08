"""__main__.py

Entry point.
"""

import sys
from argparse import ArgumentParser

from . import run_program
from .emailer import send_email
from .logger import TaskFailure, format_content, log_report

# Simple command line parser for debugging
parser = ArgumentParser(description="Manually run counters program")
parser.add_argument("-d", "--discord", action="store_true")
parser.add_argument("-i", "--instagram", action="store_true")
parser.add_argument("-s", "--spotify", action="store_true")
ns = parser.parse_args(sys.argv[1:])

# Unpack arguments
d = ns.discord
i = ns.instagram
s = ns.spotify
# If no flags were supplied, run all as default behavior
# This way it doesn't break the task set up in Task Scheduler
if not any((d, i, s)):
    d = i = s = True

# Run program
fails = TaskFailure()
run_program(fails, d, i, s)

report = format_content(fails)

# Log and send failure report is there was any error
log_report(report)
send_email(report)
