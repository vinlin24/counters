"""cli.py

Defines the entry point for the Poetry script.
"""

import logging
import sys
from argparse import ArgumentParser, ArgumentTypeError
from datetime import date, datetime
from pathlib import Path

from .core import run_counters
from .dry_run import print_dry_run
from .emailer import send_email
from .logger import TaskFailure, format_content, log_report
from .status_logger.core import run_status_logger


def valid_iso_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ArgumentTypeError(
            f"{value!r} is not a valid ISO date"
        ) from None


parser = ArgumentParser(
    description="Manually run counters program",
)

# Output to console only, don't touch log file and don't email
parser.add_argument(
    "-c", "--console",
    action="store_true",
    help="output to console only, don't touch log file and don't email",
)
# Run with a browser window instead of headlessly
parser.add_argument(
    "-w", "--window",
    action="store_true",
    help="have Selenium run with a browser window instead of headlessly",
)
# Manually specify the web driver executable
parser.add_argument(
    "-p", "--path",
    type=Path,
    help="custom path to web driver executable to use",
)
# If any of these are included, run those select tasks instead of all
parser.add_argument(
    "-d", "--discord",
    action="store_true",
    help="run the Discord task (runs all tasks if such flags omitted)",
)
parser.add_argument(
    "-i", "--instagram",
    action="store_true",
    help="run the Instagram task (runs all tasks if such flags omitted)",
)
parser.add_argument(
    "-s", "--spotify",
    action="store_true",
    help="run the Spotify tasks (runs all tasks if such flags omitted)",
)
parser.add_argument(
    "-g", "--github",
    action="store_true",
    help="run the GitHub task (runs all tasks if such flags omitted)",
)
parser.add_argument(
    "-l", "--log-discord-status",
    action="store_true",
    help="log Discord custom status instead of updating counters",
)
# Read configuration file and output what would be run
parser.add_argument(
    "-n", "--dry-run",
    nargs="?",
    type=valid_iso_date,
    const=date.today(),
    help="display the values that would be used if counters program were run",
)


def main() -> None:
    # Parse and unpack debugging options
    ns = parser.parse_args(sys.argv[1:])

    # Argument postprocessing:
    # If none of these switches were supplied, run all as default behavior
    # This way it doesn't break the task set up in Task Scheduler
    if not any((ns.discord, ns.instagram, ns.spotify, ns.github)):
        ns.discord = ns.instagram = ns.spotify = ns.github = True

    console_only: bool = ns.console
    windowed: bool = ns.window
    path: Path | None = ns.path
    d: bool = ns.discord
    i: bool = ns.instagram
    s: bool = ns.spotify
    g: bool = ns.github
    dry_run_date: date | None = ns.dry_run
    log_discord_status: bool = ns.log_discord_status

    if console_only:
        logging.disable(100)

    if dry_run_date is not None:
        print_dry_run(dry_run_date)
        sys.exit(0)

    # Run status-logger sub-program and ignore everything else.
    if log_discord_status:
        # LEFT OFF HERE: HAVEN'T TESTED.
        success = run_status_logger(console_only=console_only,
                                    headless=not windowed,
                                    driver_path=path)
        sys.exit(0 if success else 1)

    fails = TaskFailure()
    run_counters(fails, windowed, path, d, i, s, g)

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
