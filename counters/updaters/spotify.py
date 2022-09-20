"""spotify.py

Interface for updating Spotify playlist details.
"""

import tekore

from ..config import (SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,
                      SPOTIFY_USER_REFRESH)

# Authenticate
token = tekore.refresh_user_token(client_id=SPOTIFY_CLIENT_ID,
                                  client_secret=SPOTIFY_CLIENT_SECRET,
                                  refresh_token=SPOTIFY_USER_REFRESH)

# Log in as client
spotify = tekore.Spotify(token.access_token)


def update_playlist(playlist_id: str,
                    name: str | None = None,
                    description: str | None = None
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
