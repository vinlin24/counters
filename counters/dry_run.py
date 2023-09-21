"""
Prepare the output for the `--dry-run` option, which makes the program
load the configuration and display the values that WOULD be used if the
program were executed normally.
"""

from datetime import date
from typing import Any, Literal

import rich.box
import rich.traceback
from rich.console import Console
from rich.table import Table
from rich.text import Text

from .bios import (LoadedDict, get_discord_task, get_github_task,
                   get_instagram_task, get_spotify_tasks, load_json)
from .config import JSON_FILE_PATH
from .logger import get_last_success_timestamp

DISABLED_TEXT = Text("✗ DISABLED", style="red")
ENABLED_TEXT = Text("✓ ENABLED", style="green")
UNCHANGED_TEXT = Text("<unchanged>", style="black")


def format_task(
    platform: Literal["DISCORD", "INSTAGRAM", "GITHUB"],
    data: LoadedDict,
) -> Table:
    task: str | None
    color: str
    match platform:
        case "DISCORD":
            task = get_discord_task(data)
            color = "blue"
        case "INSTAGRAM":
            task = get_instagram_task(data)
            color = "bright_magenta"
        case "GITHUB":
            task = get_github_task(data)
            color = "white"

    table = Table(
        title=Text(platform, style=color),
        style=color,
    )
    # Make the enabled/disabled text appear as a "header".
    table.add_column("", justify="right")
    if task is None:
        table.add_column(DISABLED_TEXT)
        table.add_row("bio", Text("(config was `null`)", style="black"))
    else:
        table.add_column(ENABLED_TEXT)
        table.add_row("bio", task)
    return table


def format_spotify_tasks(data: LoadedDict) -> list[Table]:
    def format_spotify_task(task: dict[str, Any]) -> Table:
        playlist_id = task["playlist_id"]
        comment = task["comment"]
        if task["name"]:
            name = task['name']
        else:
            name = UNCHANGED_TEXT
        if task["description"]:
            description = task['description']
        else:
            description = UNCHANGED_TEXT

        table = Table(
            title=Text("SPOTIFY", style="green"),
            style="green",
        )
        # Make the enabled/disabled text appear as a "header".
        table.add_column("", justify="right")
        table.add_column(ENABLED_TEXT)

        table.add_row("id", Text(playlist_id, style="black"))
        table.add_row("comment", comment or "?")
        table.add_row("name", name)
        table.add_row("description", description)

        return table

    spotify_tasks = get_spotify_tasks(data)
    tables = [format_spotify_task(task) for task in spotify_tasks]

    # Prepare a single special "DISABLED" table.
    if len(tables) == 0:
        table = Table(
            title=Text("SPOTIFY", style="green"),
            style="green"
        )
        # Make the enabled/disabled text appear as a "header".
        table.add_column("", justify="right")
        table.add_column(DISABLED_TEXT)
        table.add_row("", Text("(config was `[]`)", style="black"))
        tables = [table]

    return tables


def print_dry_run() -> None:
    """Return output for the option of just reading the config file."""
    console = Console()
    rich.traceback.install(console=console)

    data = load_json()

    console.print(
        "\nThe values that will be used upon running this program "
        f"today {date.today()}, as loaded from {JSON_FILE_PATH}:\n"
    )

    for platform in ("DISCORD", "INSTAGRAM", "GITHUB"):
        table = format_task(platform, data)
        console.print(table)

    tables = format_spotify_tasks(data)
    for table in tables:
        console.print(table)

    console.print("\nTo execute, drop the `--dry-run` flag.")
    timestamp = get_last_success_timestamp()
    if timestamp is not None:
        console.print(f"[black]Last successful run at {timestamp}.[/]\n")
