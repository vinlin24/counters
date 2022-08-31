"""__main__.py

Entry point.
"""

import logging

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

from .bios import (get_discord_task, get_instagram_task, get_spotify_tasks,
                   load_json)
from .config import EDGE_DRIVER_PATH, LOG_FILE_PATH, WAIT_TIMEOUT
from .update_discord import update_status
from .update_instagram import update_bio
from .update_spotify import update_playlist

# Basic log setup

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] [%(levelname)-8s] %(filename)s:%(lineno)s:%(message)s",
    datefmt="[%X]",
    level=logging.INFO
)
log = logging.getLogger("counters")


# Load data from central JSON file

data = load_json()


# Initialize Edge driver

service = Service(str(EDGE_DRIVER_PATH))
options = Options()
options.headless = True
# Headless option by default causes window to be tiny, which interferes
# with finding elements if it's rendered responsively
options.add_argument("--window-size=1920,1080")
driver = webdriver.Edge(service=service, options=options)
driver.implicitly_wait(WAIT_TIMEOUT)

# Don't let the failure of one task stop the others

try:
    discord_status = get_discord_task(data)
    update_status(driver, discord_status)
except Exception:
    log.exception("Failed to update Discord custom status:")
else:
    log.info("Updated Discord custom status.")

try:
    instagram_bio = get_instagram_task(data)
    update_bio(driver, instagram_bio)
except Exception:
    log.exception("Failed to update Instagram bio:")
else:
    log.info("Updated Instagram bio.")

try:
    spotify_tasks = get_spotify_tasks(data)
    for task in spotify_tasks:
        update_playlist(**task)  # type: ignore
except Exception:
    log.exception("Failed to update Spotify playlists:")
else:
    log.info("Updated Spotify playlists.")

# Cleanup
driver.quit()
