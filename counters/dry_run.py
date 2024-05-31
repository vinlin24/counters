"""
Prepare the output for the `--dry-run` option, which makes the program
load the configuration and display the values that WOULD be used if the
program were executed normally.
"""

from datetime import date

import rich.box
import rich.traceback
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel

from .config import EXIT_SUCCESS, JSON_FILE_PATH
from .logger import get_last_success_timestamp
from .updaters.base import Updater

console = Console()
rich.traceback.install(console=console)


def execute_dry_run(updaters: list[Updater], date_to_simulate: date) -> int:
    """
    Encapsulation of the `--dry-run` subprogram. Given updaters, query
    their console representations and format and output them to stdout.
    Return exit code.
    """
    _print_header(date_to_simulate)
    _print_previews(updaters, date_to_simulate)
    _print_footer()
    return EXIT_SUCCESS


def _print_header(date_to_simulate: date) -> None:
    header = Panel(
        "The values that will be used upon running this program on "
        f"[bold]{date_to_simulate}[/], as loaded from {JSON_FILE_PATH}:",
        style="cyan",
        expand=True,
    )
    console.print(header)


def _print_previews(updaters: list[Updater], date_to_simulate: date) -> None:
    panels = list[Panel]()
    for updater in updaters:
        details = updater.prepare_details(date_to_simulate)
        panel = updater.format_preview(details)
        panels.append(panel)

    # +1 such that for odd numbers, the left column has one more.
    half = (len(panels) + 1) // 2
    left_column = panels[:half]
    right_column = panels[half:]

    groups = [Group(*left_column), Group(*right_column)]
    console.print(Columns(groups))


def _print_footer() -> None:
    timestamp = get_last_success_timestamp()
    if timestamp is not None:
        timestamp_text = f"\n[black]Last successful run at {timestamp}.[/]"
    else:
        timestamp_text = ""

    footer = Panel(
        "To execute, drop the `--dry-run` flag when running directly "
        f"or when scheduling.{timestamp_text}",
        expand=True,
    )
    console.print(footer)
