"""cli.py

Defines the entry point for the Poetry script.
"""

import sys
from datetime import date
from pathlib import Path

from . import parse_args, run_program
from .dry_run import print_dry_run
from .emailer import send_email
from .logger import TaskFailure, format_content, log_report, logging


def main() -> None:
    # Parse and unpack debugging options
    ns = parse_args()
    console_only: bool = ns.console
    windowed: bool = ns.window
    path: Path | None = ns.path
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
    run_program(fails, windowed, path, d, i, s, g)

    # Log and send failure report is there was any error
    if not console_only:
        report = format_content(fails, d, i, s, g)
        log_report(report)
        send_email(report)
    else:
        fails.print_tracebacks()

    # So the scheduler conveys the failure too.
    sys.exit(0 if fails.all_good() else 1)


if __name__ == "__main__":
    main()
