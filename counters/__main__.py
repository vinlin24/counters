from .bios import get_spotify_tasks, load_json
from .update_spotify import update_playlist

data = load_json()
spotify_tasks = get_spotify_tasks(data)
for task in spotify_tasks:
    update_playlist(**task)  # type: ignore
