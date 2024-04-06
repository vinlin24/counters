"""spotify.py

Interface for updating Spotify playlist details.
"""

from datetime import date
from typing import TypedDict

import tekore
from rich.panel import Panel
from selenium import webdriver

from ..bios import day_number
from ..config import (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                      SPOTIFY_USER_REFRESH)
from ..updaters.base import Updater


class PlaylistDetails(TypedDict):
    id: str
    name: str | None
    description: str | None


class SpotifyDetails(TypedDict):
    playlists: list[PlaylistDetails]


class SpotifyUpdater(Updater[SpotifyDetails]):
    def __init__(self, data: dict, driver: webdriver.Edge) -> None:
        super().__init__(data, driver)
        token = tekore.refresh_user_token(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET,
            refresh_token=SPOTIFY_USER_REFRESH,
        )
        self.spotify = tekore.Spotify(token.access_token)

    def prepare_details(self, today: date) -> SpotifyDetails:
        tasks: list[dict] = self.data["spotify"]

        playlist_details = list[PlaylistDetails]()
        for task in tasks:
            # Fill day number placeholders if included
            name: str | None = task["name"]
            description: str | None = task["description"]
            start: date | None = task["start"]
            # comment: str | None = task.get("comment")

            if start is not None:
                if name is not None:
                    name = name.format(day_number(start, today))
                if description is not None:
                    description = description.format(day_number(start, today))

            one_playlist_details: PlaylistDetails = {
                "id": task["playlist_id"],
                "name": name,
                "description": description,
            }
            playlist_details.append(one_playlist_details)

        return {"playlists": playlist_details}

    # TODO: This is a problem. Based on the uniform interface,
    # update_bio has to update ALL playlists at once. But this breaks
    # some existing things. Notably, error collection can no longer be
    # granular at the playlist level since update_bio() black-boxes the
    # updating of all playlists at once...
    def update_bio(self, details: SpotifyDetails) -> None:
        for one_playlist_details in details["playlists"]:
            playlist_id = one_playlist_details["id"]
            name = one_playlist_details["name"]
            description = one_playlist_details["description"]
            self.spotify.playlist_change_details(
                playlist_id=playlist_id,
                name=name,  # type: ignore
                description=description,  # type: ignore
            )

    def format_preview(self, details: SpotifyDetails) -> Panel:
        return Panel("TODO")  # TODO: figure out the playlist stuff.


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
