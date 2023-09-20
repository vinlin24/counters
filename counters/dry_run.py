from colorama import Fore

from .bios import (get_discord_task, get_github_task, get_instagram_task,
                   get_spotify_tasks, load_json)


def get_config_output() -> str:
    """Return output for the option of just reading the config file."""
    data = load_json()
    lines: list[str] = []

    discord_task = get_discord_task(data)
    instagram_task = get_instagram_task(data)
    spotify_tasks = get_spotify_tasks(data)
    github_task = get_github_task(data)

    DISABLED_TEXT = f"{Fore.RED}Disabled{Fore.RESET}"
    ENABLED_TEXT = f"{Fore.GREEN}Enabled{Fore.RESET}"
    UNCHANGED_TEXT = f"{Fore.BLACK}<unchanged>{Fore.RESET}"

    # TODO: Maybe make each of Discord, Instagram, etc. into its own
    # class to somehow separate this kind of formmating to their own
    # implementation of choice.
    for platform, task in zip(("DISCORD", "INSTAGRAM", "GITHUB"),
                              (discord_task, instagram_task, github_task)):
        if task is None:
            lines.append(f"❌ {platform}: {DISABLED_TEXT}\n"
                         f"{Fore.BLACK}(config was `null`){Fore.RESET}")
        else:
            segment = (
                f"✅ {platform}: {ENABLED_TEXT}\n"
                f"bio={Fore.YELLOW}{task!r}{Fore.RESET}"
            )
            lines.append(segment)
    result = "\n\n".join(lines)

    if len(spotify_tasks) == 0:
        result += f"\n\n❌ SPOTIFY: {DISABLED_TEXT} (config was `[]`)"
        return result

    lines: list[str] = []
    for task in spotify_tasks:
        playlist_id = task["playlist_id"]
        comment = task["comment"]
        if task["name"]:
            name = f"{Fore.YELLOW}{task['name']!r}{Fore.RESET}"
        else:
            name = UNCHANGED_TEXT
        if task["description"]:
            description = f"{Fore.YELLOW}{task['description']!r}{Fore.RESET}"
        else:
            description = UNCHANGED_TEXT
        segment = (
            f"✅ SPOTIFY: {ENABLED_TEXT} ({comment or '?'})\n"
            f"id={Fore.BLACK}{playlist_id}{Fore.RESET}\n"
            f"name={name}\n"
            f"description={description}"
        )
        lines.append(segment)
    result += "\n\n" + "\n\n".join(lines)
    return result
