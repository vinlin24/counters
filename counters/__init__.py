"""__init__.py

Expose the main process to run as a function.
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

from .bios import (get_discord_task, get_instagram_task, get_spotify_tasks,
                   load_json)
from .config import EDGE_DRIVER_PATH, WAIT_TIMEOUT
from .emailer import TaskFailure
from .update_discord import update_status
from .update_instagram import update_bio
from .update_spotify import update_playlist


def run_program(fails: TaskFailure) -> None:
    """Run the main process.

    Args:
        fails (TaskFailure): Dataclass whose fields record errors, if
        any, for individual tasks within this function.
    """
    # Load data from central JSON file
    try:
        data = load_json()
    except Exception as e:
        fails.json = e
        return

    # Initialize Edge driver
    try:
        service = Service(str(EDGE_DRIVER_PATH))
        options = Options()
        options.headless = True
        # Headless option by default causes window to be tiny, which interferes
        # with finding elements if it's rendered responsively
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Edge(service=service, options=options)
        driver.implicitly_wait(WAIT_TIMEOUT)
    except Exception as e:
        fails.driver = e
        return

    # Don't let the failure of one task stop the others
    # Compile the raised exceptions in the TaskFailure instance instead
    try:
        discord_status = get_discord_task(data)
        update_status(driver, discord_status)
    except Exception as e:
        fails.discord = e

    try:
        instagram_bio = get_instagram_task(data)
        update_bio(driver, instagram_bio)
    except Exception as e:
        fails.instagram = e

    try:
        spotify_tasks = get_spotify_tasks(data)
    except Exception as e:
        fails.spotify[None] = e
    else:
        for task in spotify_tasks:
            try:
                update_playlist(**task)  # type: ignore
            except Exception as e:
                playlist_id = task["playlist_id"]
                fails.spotify[playlist_id] = e

    # Cleanup
    driver.quit()
