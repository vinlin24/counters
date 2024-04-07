from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.text import Text

DISABLED_TEXT = Text("✗ DISABLED", style=Style(color="red", bold=True))
ENABLED_TEXT = Text("✓ ENABLED", style=Style(color="green", bold=True))
UNCHANGED_TEXT = Text("<unchanged>", style=Style(color="black"))


def format_generic_task_preview(
    *,
    platform_name: str,
    body: RenderableType | None,
    color: StyleType,
) -> Panel:
    header = (DISABLED_TEXT if body is None else ENABLED_TEXT).copy()
    header.justify = "right"

    null_text = Text("(config was `null`)", style="black")
    panel = Panel(
        null_text if body is None else body,
        style=color,
    )

    return Panel(
        Group(header, panel),
        title=Text(platform_name.upper(), style=color),
        title_align="left",
        style=color,
        expand=True,
    )
