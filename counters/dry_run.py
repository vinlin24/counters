"""
Prepare the output for the `--dry-run` option, which makes the program
load the configuration and display the values that WOULD be used if the
program were executed normally.
"""

from datetime import date
from typing import Any, Literal

import rich.box
import rich.traceback
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from .bios import (LoadedDict, get_discord_task, get_github_task,
                   get_instagram_task, get_spotify_tasks, load_json)
from .config import JSON_FILE_PATH
from .logger import get_last_success_timestamp

DISABLED_TEXT = Text("✗ DISABLED", style=Style(color="red", bold=True))
ENABLED_TEXT = Text("✓ ENABLED", style=Style(color="green", bold=True))
UNCHANGED_TEXT = Text("<unchanged>", style=Style(color="black"))


def format_task(
    platform: Literal["DISCORD", "INSTAGRAM", "GITHUB"],
    data: LoadedDict,
    today: date,
) -> Panel:
    task: str | None
    color: str
    match platform:
        case "DISCORD":
            task = get_discord_task(data, today)
            color = "blue"
        case "INSTAGRAM":
            task = get_instagram_task(data, today)
            color = "bright_magenta"
        case "GITHUB":
            task = get_github_task(data, today)
            color = "white"

    header = (DISABLED_TEXT if task is None else ENABLED_TEXT).copy()
    header.justify = "right"

    null_text = Text("(config was `null`)", style="black")
    body = Panel(
        null_text if task is None else Text(task, style="reset"),
        style=color,
    )

    return Panel(
        Group(header, body),
        title=Text(platform, style=color),
        title_align="left",
        style=color,
        expand=True,
    )


def format_spotify_tasks(data: LoadedDict, today: date) -> list[Panel]:
    def format_spotify_task(task: dict[str, Any]) -> Panel:
        playlist_id = task["playlist_id"]
        comment = Text(task["comment"])
        if task["name"]:
            name = Text(task["name"])
        else:
            name = UNCHANGED_TEXT
        if task["description"]:
            description = Text(task["description"])
        else:
            description = UNCHANGED_TEXT

        header = (DISABLED_TEXT if task is None else ENABLED_TEXT).copy()
        header.justify = "right"

        table = Table(style="green", show_header=False, expand=True)
        table.add_column("", style="reset", justify="right")
        table.add_column("", style="reset")
        table.add_row("id", Text(playlist_id, style="black"))
        table.add_row("comment", comment or "?")
        table.add_row("name", name)
        table.add_row("description", description)

        return Panel(
            Group(header, table),
            title=Text("SPOTIFY Playlist", style="green"),
            title_align="left",
            style="green",
            expand=True,
        )

    spotify_tasks = get_spotify_tasks(data, today)
    panels = [format_spotify_task(task) for task in spotify_tasks]

    # Prepare a single special "DISABLED" panel.
    if len(panels) == 0:
        header = DISABLED_TEXT.copy()
        header.justify = "right"
        panel = Panel(
            Group(header, Panel(Text("(config was `[]`)", style="black"))),
            title=Text("SPOTIFY Playlist", style="green"),
            title_align="left",
            style="green",
            expand=True,
        )

        panels = [panel]

    return panels


def print_dry_run(simulation_date: date) -> None:
    """Return output for the option of just reading the config file."""
    console = Console()
    rich.traceback.install(console=console)

    data = load_json()

    header = Panel(
        "The values that will be used upon running this program on "
        f"[bold]{simulation_date}[/], as loaded from {JSON_FILE_PATH}:",
        style="cyan",
        expand=True,
    )
    console.print(header)

    columns: tuple[list[Panel], list[Panel]] = ([], [])

    for platform in ("DISCORD", "INSTAGRAM", "GITHUB"):
        panel = format_task(platform, data, simulation_date)
        columns[0].append(panel)

    panels = format_spotify_tasks(data, simulation_date)
    for panel in panels:
        columns[1].append(panel)

    groups = [Group(*columns[0]), Group(*columns[1])]
    console.print(Columns(groups), justify="center")

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
