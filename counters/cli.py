"""cli.py

Defines the entry point for the Poetry script.
"""

import logging
import sys
from argparse import ArgumentParser, ArgumentTypeError
from datetime import date, datetime, timedelta
from pathlib import Path

from .config import EXIT_FAILURE_STATUS_LOGGER, EXIT_SUCCESS, ProgramOptions
from .core import CountersProgram
from .status_logger.core import run_status_logger


def valid_date(value: str) -> date:
    """
    Transform `value` into a date if possible, else raise
    `argparse.ArgumentTypeError`.

    Currently recognized date formats are ISO 8601 and certain
    convenience literals e.g. `"tomorrow"`.
    """
    value = value.strip().lower()

    # First try special literals.
    if value in {"tomorrow", "tmrw", "tmr"}:
        tomorrow = date.today() + timedelta(days=1)
        return tomorrow
    if value in {"today"}:
        return date.today()

    # Then try ISO 8601.
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        raise ArgumentTypeError(
            f"{value!r} is not a valid ISO date"
        ) from None


parser = ArgumentParser(
    description="Manually run counters program",
)

parser.add_argument(
    "date_to_update_to",
    nargs="?",
    type=valid_date,
    default=date.today(),
    help="date to update counters to (defaults to today)",
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
    type=valid_date,
    const=date.today(),
    help="display the values that would be used if counters program were run",
)
parser.add_argument(
    "-1",
    dest="dry_run_one_per_line",
    action="store_true",
    help="display dry-run values one entry per line",
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
        date_to_update_to=args.date_to_update_to,
        console_only=args.console,
        windowed=args.window,
        driver_path=args.path,
        run_discord=args.discord,
        run_instagram=args.instagram,
        run_spotify=args.spotify,
        run_github=args.github,
        dry_run_date=args.dry_run,
        log_discord_status=args.log_discord_status,
        dry_run_one_per_line=args.dry_run_one_per_line,
    )


def main() -> None:
    options = get_options()

    if options.console_only:
        logging.disable(100)

    # Run status-logger sub-program and ignore everything else.
    if options.log_discord_status:
        success = run_status_logger(console_only=options.console_only,
                                    headless=not options.windowed,
                                    driver_path=options.driver_path)
        sys.exit(EXIT_SUCCESS if success else EXIT_FAILURE_STATUS_LOGGER)

    # Run the main program.
    counters = CountersProgram(options)
    exit_code = counters.run()

    # So the scheduler/script conveys the failure too.
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
