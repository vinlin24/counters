"""__main__.py

Entry point.
"""

from .bios import get_instagram_task, get_spotify_tasks, load_json
from .update_instagram import update_bio
from .update_spotify import update_playlist

data = load_json()

instagram_bio = get_instagram_task(data)
update_bio(instagram_bio)

print("Updated Instagram bio.")

spotify_tasks = get_spotify_tasks(data)
for task in spotify_tasks:
    update_playlist(**task)  # type: ignore

print("Updated Spotify playlists.")
