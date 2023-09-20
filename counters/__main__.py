"""__main__.py

Entry point.
"""

import sys
from datetime import date

from colorama import Fore

from . import parse_args, run_program
from .bios import get_config_output
from .config import JSON_FILE_PATH
from .emailer import send_email
from .logger import (TaskFailure, format_content, get_last_success_timestamp,
                     log_report, logging)

# Parse and unpack debugging options
ns = parse_args()
console_only: bool = ns.console
windowed: bool = ns.window
d: bool = ns.discord
i: bool = ns.instagram
s: bool = ns.spotify
g: bool = ns.github
dry_run: bool = ns.dry_run

if console_only:
    logging.disable(100)

if dry_run:
    output_lines = get_config_output().splitlines()
    # Indent between the header and footer for a cooler effect I guess
    output_lines = [f"    {line}" for line in output_lines]
    print(
        "\nThe values that will be used upon running this program "
        f"today {date.today()}, as loaded from {JSON_FILE_PATH}:\n"
    )
    print("\n".join(output_lines))
    print("\nTo execute, drop the `--dry-run` flag.")
    timestamp = get_last_success_timestamp()
    print(f"{Fore.BLACK}Last successful run was at {timestamp}.{Fore.RESET}\n")
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
