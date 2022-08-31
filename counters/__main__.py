"""__main__.py

Entry point.
"""

from .bios import (get_discord_task, get_instagram_task, get_spotify_tasks,
                   load_json)
from .update_discord import update_status
from .update_instagram import update_bio
from .update_spotify import update_playlist

data = load_json()

# Don't let the failure of one task stop the others

try:
    discord_status = get_discord_task(data)
    update_status(discord_status)
except Exception:
    print("Failed to update Discord custom status.")
else:
    print("Updated Discord custom status.")

try:
    instagram_bio = get_instagram_task(data)
    update_bio(instagram_bio)
except Exception:
    print("Failed to update Instagram bio.")
else:
    print("Updated Instagram bio.")

try:
    spotify_tasks = get_spotify_tasks(data)
    for task in spotify_tasks:
        update_playlist(**task)  # type: ignore
except Exception:
    print("Failed to update Spotify playlists.")
else:
    print("Updated Spotify playlists.")
