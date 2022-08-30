"""config.py

Load and expose configuration options as constants.
"""

import os

import dotenv

# Load environment variables if .env file is set up
dotenv.load_dotenv(override=True)


# ==================== DISCORD ==================== #

DISCORD_EMAIL = os.environ["DISCORD_EMAIL"]
DISCORD_PASSWORD = os.environ["DISCORD_PASSWORD"]


# ==================== INSTAGRAM ==================== #

INSTAGRAM_USERNAME = os.environ["INSTAGRAM_USERNAME"]
INSTAGRAM_PASSWORD = os.environ["INSTAGRAM_PASSWORD"]


# ==================== SPOTIFY ==================== #

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = os.environ["SPOTIFY_REDIRECT_URI"]
SPOTIFY_USER_REFRESH = os.environ["SPOTIFY_USER_REFRESH"]
