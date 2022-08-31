#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
coding_mix.py
11 June 2022 10:18:29

Simple script to increment the day count of my coding mix playlist on Spotify.
"""

import ctypes
import functools
import json
import traceback
from datetime import date

import tekore as tk
from dotenv import load_dotenv
from win10toast_click import ToastNotifier

# Read/write preferences
tk.client_id_var = "SPOTIFY_CLIENT_ID"
tk.client_secret_var = "SPOTIFY_CLIENT_SECRET"
tk.redirect_uri_var = "SPOTIFY_REDIRECT_URI"
tk.user_refresh_var = "SPOTIFY_REFRESH_TOKEN"

# "coding mix" (previously known as "read access violation")
PLAYLIST_ID = "5FpuSaX0kDeItlPMIIYBZS"
START_DATE = date(2022, 6, 11)
BIOS_PATH = "../bios.json"

with open(BIOS_PATH, "rt") as file:
    bios: dict[str, str] = json.load(file)

DESCRIPTION_TEMPLATE = bios["spotify"]


def load_config() -> tuple[str, str, str, str]:
    """Return application credentials.

    Tuple is in the form of (client ID, client secret, redirect URI, user refresh token).
    """
    load_dotenv()
    return tk.config_from_environment(return_refresh=True)


def login() -> tk.Spotify:
    """Login as Vincent Lin (username: pqsb8efk8cbhkei8p5sn7za13) and return client."""
    client_id, client_secret, _, user_refresh = load_config()
    token = tk.refresh_user_token(client_id, client_secret, user_refresh)
    return tk.Spotify(token.access_token)


def day_number() -> int:
    """Return day number since start, with START_DATE as Day 1."""
    return (date.today() - START_DATE).days + 1  # +1 to start at Day 1


def increment_day_count(spotify: tk.Spotify) -> None:
    """Increment the playlist description."""
    new_description = DESCRIPTION_TEMPLATE.format(day_num=day_number())
    spotify.playlist_change_details(PLAYLIST_ID, description=new_description)


def show_error(e: Exception) -> None:
    """Display traceback in a Windows message box."""
    # Magic from https://stackoverflow.com/questions/4485610/python-message-box-without-huge-library-dependency.
    MessageBox = ctypes.windll.user32.MessageBoxW
    # Idea from https://stackoverflow.com/questions/11414894/extract-traceback-info-from-an-exception-object.
    tb_str = "".join(traceback.format_tb(e.__traceback__))
    error_msg = "\n".join((
        "Traceback (most recent call last):",
        tb_str,
        f"{type(e).__name__}: {e}"
    ))
    MessageBox(None, error_msg, "Error in coding_mix.py", 0)


def main() -> None:
    """Main driver function."""
    try:
        spotify = login()
        increment_day_count(spotify)
    except Exception as e:
        toaster = ToastNotifier()
        toaster.show_toast("coding_mix.py",
                           "Something went wrong!",
                           icon_path="dialog_error_icon.ico",
                           duration=3,
                           threaded=True,
                           callback_on_click=functools.partial(show_error, e))
        return


if __name__ == "__main__":
    main()
