"""spotify.py

Interface for updating Spotify playlist details.
"""

from datetime import date
from typing import TypedDict

import tekore
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ..bios import day_number
from ..config import (PLATFORM_SPOTIFY, SPOTIFY_CLIENT_ID,
                      SPOTIFY_CLIENT_SECRET, SPOTIFY_USER_REFRESH)
from ..updaters.base import Updater
from ..utils import UNCHANGED_TEXT, format_generic_task_preview

# Refresh token and instantiate client once to minimize API calls.
_token = tekore.refresh_user_token(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    refresh_token=SPOTIFY_USER_REFRESH,
)
_spotify = tekore.Spotify(_token.access_token)


class SpotifyPlaylistDetails(TypedDict):
    id: str
    name: str | None
    description: str | None
    comment: str | None


class SpotifyPlaylistUpdater(Updater[SpotifyPlaylistDetails]):
    @property
    def platform_name(self) -> str:
        return f"{PLATFORM_SPOTIFY} Playlist (ID={self.data['playlist_id']})"

    def prepare_details(self, today: date) -> SpotifyPlaylistDetails:
        # Fill day number placeholders if included
        name: str | None = self.data["name"]
        description: str | None = self.data["description"]
        start: date | None = self.data["start"]
        comment: str | None = self.data.get("comment")

        if start is not None:
            if name is not None:
                name = name.format(day_number(start, today))
            if description is not None:
                description = description.format(day_number(start, today))

        playlist_details: SpotifyPlaylistDetails = {
            "id": self.data["playlist_id"],
            "name": name,
            "description": description,
            "comment": comment,
        }
        return playlist_details

    def update_bio(self, details: SpotifyPlaylistDetails, _) -> None:
        playlist_id = details["id"]
        name = details["name"]
        description = details["description"]
        _spotify.playlist_change_details(
            playlist_id=playlist_id,
            name=name,  # type: ignore
            description=description,  # type: ignore
        )

    def format_preview(self, details: SpotifyPlaylistDetails) -> Panel:
        playlist_id = details["id"]
        comment = Text(details.get("comment") or "?")
        if details["name"]:
            name = Text(details["name"])
        else:
            name = UNCHANGED_TEXT
        if details["description"]:
            description = Text(details["description"])
        else:
            description = UNCHANGED_TEXT

        table = Table(style="green", show_header=False, expand=True)
        table.add_column("", style="reset", justify="right")
        table.add_column("", style="reset")
        table.add_row("id", Text(playlist_id, style="black"))
        table.add_row("comment", comment)
        table.add_row("name", name)
        table.add_row("description", description)

        return format_generic_task_preview(
            platform_name="Spotify Playlist",
            body=table,
            color="green",
        )


# TODO: Replace below when finished refactoring other modules.


# Authenticate
token = tekore.refresh_user_token(client_id=SPOTIFY_CLIENT_ID,
                                  client_secret=SPOTIFY_CLIENT_SECRET,
                                  refresh_token=SPOTIFY_USER_REFRESH)

# Log in as client
spotify = tekore.Spotify(token.access_token)


def update_playlist(playlist_id: str,
                    name: str | None = None,
                    description: str | None = None,
                    **kwargs,  # Ignore extraneous config like `comment`
                    ) -> None:
    """Update Spotify playlist details.

    Args:
        playlist_id (str): ID of the playlist to update.
        name (str | None, optional): New name of the playlist. Defaults
        to None, meaning keep the current name.
        description (str | None, optional): New description of the
        playlist. Defaults to None, meaning keep the current
        description.
    """
    spotify.playlist_change_details(playlist_id=playlist_id,
                                    name=name,  # type: ignore
                                    description=description)  # type: ignore
