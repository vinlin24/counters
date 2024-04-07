"""config.py

Load and expose configuration options as constants.
"""

import os
from dataclasses import dataclass
from datetime import date
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


# ==================== EXIT CODES/BITFLAGS ==================== #

# Bits:
# 5 4 3 2   1 0
# _ _ _ _ | _ _
# G S I D
# ^^^^^^^   ^^^
#  tasks  general

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EXIT_FAILURE_STATUS_LOGGER = 2

EXIT_FAILURE_DISCORD = 1 << 2
EXIT_FAILURE_INSTAGRAM = 1 << 3
EXIT_FAILURE_SPOTIFY = 1 << 4
EXIT_FAILURE_GITHUB = 1 << 5


# ==================== PROGRAM OPTIONS ==================== #

@dataclass
class ProgramOptions:
    """
    Program options, post-processed from the command line as needed.
    """
    console_only: bool
    windowed: bool
    driver_path: Path | None
    run_discord: bool
    run_instagram: bool
    run_spotify: bool
    run_github: bool
    dry_run_date: date | None
    log_discord_status: bool
