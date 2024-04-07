"""cli.py

Defines the entry point for the Poetry script.
"""

import logging
import sys
from argparse import ArgumentParser, ArgumentTypeError
from datetime import date, datetime
from pathlib import Path

from .config import EXIT_FAILURE_STATUS_LOGGER, EXIT_SUCCESS, ProgramOptions
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

# Meta arguments.

parser.add_argument(
    "-c", "--console",
    action="store_true",
    help="output to console only, don't touch log file and don't email",
)
parser.add_argument(
    "-w", "--window",
    action="store_true",
    help="have Selenium run with a browser window instead of headlessly",
)
parser.add_argument(
    "-p", "--path",
    type=Path,
    help="custom path to web driver executable to use",
)

# Special modes.

parser.add_argument(
    "-n", "--dry-run",
    nargs="?",
    type=valid_iso_date,
    const=date.today(),
    help="display the values that would be used if counters program were run",
)
parser.add_argument(
    "-l", "--log-discord-status",
    action="store_true",
    help="log Discord custom status instead of updating counters",
)

# Supported platforms. If any of these are included, run those select
# tasks instead of all.

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


def get_options() -> ProgramOptions:
    # Parse and unpack debugging options.
    args = parser.parse_args()

    # Argument postprocessing: If none of these switches were supplied,
    # run all as default behavior This way it doesn't break the task set
    # up in Task Scheduler.
    if not any((args.discord, args.instagram, args.spotify, args.github)):
        args.discord = args.instagram = args.spotify = args.github = True

    return ProgramOptions(
        console_only=args.console,
        windowed=args.window,
        driver_path=args.path,
        run_discord=args.discord,
        run_instagram=args.instagram,
        run_spotify=args.spotify,
        run_github=args.github,
        dry_run_date=args.dry_run,
        log_discord_status=args.log_discord_status,
    )


def main() -> None:
    options = get_options()

    if options.console_only:
        logging.disable(100)

    if options.dry_run_date is not None:
        print_dry_run(options.dry_run_date)
        sys.exit(EXIT_SUCCESS)

    # Run status-logger sub-program and ignore everything else.
    if options.log_discord_status:
        success = run_status_logger(console_only=options.console_only,
                                    headless=not options.windowed,
                                    driver_path=options.driver_path)
        sys.exit(EXIT_SUCCESS if success else EXIT_FAILURE_STATUS_LOGGER)

    fails = TaskFailure()
    run_counters(
        fails,
        options.windowed,
        options.driver_path,
        options.run_discord,
        options.run_instagram,
        options.run_spotify,
        options.run_github,
    )

    # Log and send failure report is there was any error
    if not options.console_only:
        report = format_content(
            fails,
            options.run_discord,
            options.run_instagram,
            options.run_spotify,
            options.run_github,
        )
        log_report(report)
        send_email(report)
    else:
        fails.print_tracebacks()

    # So the scheduler conveys the failure too.
    sys.exit(fails.get_exit_code())


if __name__ == "__main__":
    main()
