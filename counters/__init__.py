"""__init__.py

Expose the main process to run as a function.
"""

import sys
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from datetime import date, datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# TODO: Somehow combine the get_* and update_* functions to not clutter
from .bios import (get_discord_task, get_github_task, get_instagram_task,
                   get_spotify_tasks, load_json)
from .config import WAIT_TIMEOUT
from .logger import TaskFailure
from .updaters import (update_bio, update_playlist, update_profile_bio,
                       update_status)


def parse_args() -> Namespace:
    """Parse and process command line options for debugging.

    Returns:
        Namespace: Object with 5 fields:

        - console (bool): Output to console only, don't touch log file
        and don't email.
        - window (bool): Have Selenium run with a browser window
        instead of headlessly
        - path (Path): Custom path to web driver executable to use.
        - discord (bool): See below.
        - instagram (bool): See below.
        - spotify (bool): See below.
        - github (bool): If any of these 4 switches are included, run
        these select tasks. Otherwise if all 4 switches are absent from
        the command line, use the default behavior of running all.

    Postcondition:
        The values of these switches are not necessarily the same as
        the values in the original Namespace returned by parse_args().
        This function is responsible for some postprocessing, namely
        setting discord = instagram = spotify = github = True when all
        4 are absent from the command line.
    """
    parser = ArgumentParser(description="Manually run counters program")

    # Output to console only, don't touch log file and don't email
    parser.add_argument("-c", "--console", action="store_true")
    # Run with a browser window instead of headlessly
    parser.add_argument("-w", "--window", action="store_true")
    # Manually specify the web driver executable
    parser.add_argument("-p", "--path", type=Path)
    # If any of these are included, run those select tasks instead of all
    parser.add_argument("-d", "--discord", action="store_true")
    parser.add_argument("-i", "--instagram", action="store_true")
    parser.add_argument("-s", "--spotify", action="store_true")
    parser.add_argument("-g", "--github", action="store_true")

    def valid_iso_date(value: str) -> date:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise ArgumentTypeError(
                f"{value!r} is not a valid ISO date"
            ) from None

    # Read configuration file and output what would be run
    parser.add_argument("-n", "--dry-run", nargs="?",
                        type=valid_iso_date, const=date.today())
    ns = parser.parse_args(sys.argv[1:])

    # Argument postprocessing:
    # If none of these switches were supplied, run all as default behavior
    # This way it doesn't break the task set up in Task Scheduler
    if not any((ns.discord, ns.instagram, ns.spotify, ns.github)):
        ns.discord = ns.instagram = ns.spotify = ns.github = True

    return ns


def run_program(fails: TaskFailure,
                windowed: bool,
                path: Path | None,
                discord: bool,
                instagram: bool,
                spotify: bool,
                github: bool,
                ) -> None:
    """Run the main process.

    Args:
        fails (TaskFailure): Dataclass whose fields record errors, if
        any, for individual tasks within this function.
        windowed (bool): Whether to run the driver with a browser
        window instead of headlessly.
        path (Path | None): Path to web driver executable, if specified.
        discord (bool): Whether to run the Discord task.
        instagram (bool): Whether to run the Instagram task.
        spotify (bool): Whether to run the Spotify tasks.
        github (bool); Whether to run the GitHub task.
    """
    # Load data from central JSON file
    try:
        data = load_json()
        print("JSON data loaded.")
    except Exception as e:
        print("FAILED to load JSON data.")
        fails.json = e
        return

    # Initialize Edge driver
    try:
        if path is None:
            driver_path = EdgeChromiumDriverManager().install()
        else:
            driver_path = str(path)
        service = Service(executable_path=driver_path)
        options = Options()
        if not windowed:
            options.add_argument("--headless")
        # Headless option by default causes window to be tiny, which interferes
        # with finding elements if it's rendered responsively
        # print(f"Using profile at {PROFILE_PATH}")
        # options.add_argument(f"user-data-dir={PROFILE_PATH}")
        # print(f"Using User-Agent={USER_AGENT}")
        # options.add_argument(f"user-agent={USER_AGENT}")
        driver = webdriver.Edge(service=service, options=options)
        driver.implicitly_wait(WAIT_TIMEOUT)
        driver.maximize_window()
        print("Driver initialized.")
    except Exception as e:
        print("FAILED to initialize driver.")
        fails.driver = e
        return

    # Don't let the failure of one task stop the others
    # Compile the raised exceptions in the TaskFailure instance instead

    if discord:
        try:
            discord_status = get_discord_task(data)
            update_status(driver, discord_status)
            print("Updated Discord custom status.")
        except Exception as e:
            print("FAILED to update Discord custom status.")
            fails.discord = e

    if instagram:
        try:
            instagram_bio = get_instagram_task(data)
            update_bio(driver, instagram_bio)
            print("Updated Instagram bio.")
        except Exception as e:
            print("FAILED to update Instagram bio.")
            fails.instagram = e

    if spotify:
        try:
            spotify_tasks = get_spotify_tasks(data)
        except Exception as e:
            fails.spotify[None] = e
        else:
            for task in spotify_tasks:
                playlist_id = task["playlist_id"]
                try:
                    update_playlist(**task)  # type: ignore
                    print(f"Updated Spotify playlist with ID={playlist_id}.")
                except Exception as e:
                    print(
                        f"FAILED to update Spotify playlist with ID={playlist_id}.")
                    fails.spotify[playlist_id] = e

    if github:
        try:
            github_bio = get_github_task(data)
            update_profile_bio(github_bio)
            print("Updated GitHub bio.")
        except Exception as e:
            print("FAILED to update GitHub bio.")
            fails.github = e

    # Cleanup
    driver.quit()
