"""config.py

Load and expose configuration options as constants.
"""

import os
from pathlib import Path

import dotenv

# Load environment variables if .env file is set up
dotenv.load_dotenv(override=True)


# ==================== CENTRAL FILES ==================== #

JSON_FILE_PATH = Path.home() / ".config" / "counters" / "bios.json"
DATE_FORMAT = "%Y-%m-%d"


# ==================== SELENIUM ==================== #

EDGE_DRIVER_PATH = Path(__file__).parent / "msedgedriver.exe"
"""Absolute path to my Edge web driver executable.

Changed: Include executable in package itself instead of a path
specific to my local machine.

NOTE: The executable has to be replaced with a newer version every time
the Edge web browser is updated such that the driver and the browser
applicatin are compatible with each other.
"""

WAIT_TIMEOUT = 5.0
"""Time in seconds to implicitly wait for a webpage to load."""


# ==================== CREDENTIALS ==================== #

DISCORD_EMAIL = os.environ["DISCORD_EMAIL"]
DISCORD_PASSWORD = os.environ["DISCORD_PASSWORD"]

INSTAGRAM_USERNAME = os.environ["INSTAGRAM_USERNAME"]
INSTAGRAM_PASSWORD = os.environ["INSTAGRAM_PASSWORD"]

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
SPOTIFY_USER_REFRESH = os.environ["SPOTIFY_USER_REFRESH"]

ERROR_EMAIL = os.environ["ERROR_EMAIL"]
"""My email to send and receive error reports."""

ERROR_EMAIL_PASSWORD = os.environ["ERROR_EMAIL_PASSWORD"]
"""Password to ERROR_EMAIL."""
