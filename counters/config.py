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

LOG_FILE_PATH = Path.home() / ".config" / "counters" / "counters.log"
"""Log file to print to."""


# ==================== SELENIUM ==================== #

EDGE_DRIVER_PATH = Path("C:/Users/soula/AppData/Local/Programs/Python/"
                        "Python310/Scripts/MicrosoftWebDriver.exe")
"""Absolute path to my Edge web driver executable."""

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
