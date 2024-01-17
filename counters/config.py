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
"""Absolute path to the central JSON file containing status templates."""

JSON_SCHEMA_PATH = Path(__file__).parent / "schema" / "bios.schema.json"
"""Absolute path to the schema for the central JSON file."""

DATE_FORMAT = "%Y-%m-%d"
"""String format to encode dates in the central JSON file."""

LOG_FILE_PATH = JSON_FILE_PATH.parent / "counters.log"
"""Absolute path to the program log file."""


# ==================== SELENIUM ==================== #

WAIT_TIMEOUT = 15.0
"""Time in seconds to implicitly wait for a webpage to load."""


# ==================== CREDENTIALS ==================== #

DISCORD_EMAIL = os.environ["DISCORD_EMAIL"]
"""Email address associated with my Discord account."""
DISCORD_PASSWORD = os.environ["DISCORD_PASSWORD"]
"""Password to my Discord account."""

INSTAGRAM_USERNAME = os.environ["INSTAGRAM_USERNAME"]
INSTAGRAM_PASSWORD = os.environ["INSTAGRAM_PASSWORD"]

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
SPOTIFY_USER_REFRESH = os.environ["SPOTIFY_USER_REFRESH"]

GITHUB_PAT = os.environ["GITHUB_PAT"]
"""GitHub personal access token."""

ERROR_EMAIL = os.environ["ERROR_EMAIL"]
"""My email to send and receive error reports."""

ERROR_EMAIL_PASSWORD = os.environ["ERROR_EMAIL_PASSWORD"]
"""Password to ERROR_EMAIL."""

# PROFILE_PATH = os.environ["PROFILE_PATH"]
# """Full path to browser profile to use."""

# USER_AGENT = os.environ["USER_AGENT"]
# """User-Agent string to use."""
