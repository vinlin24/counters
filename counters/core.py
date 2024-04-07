# pylint: disable=broad-exception-caught

from datetime import date

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .config import JSON_FILE_PATH, WAIT_TIMEOUT, ProgramOptions
from .loader import load_bio_config_json
from .logger import FailureLog
from .updaters.base import Updater
from .updaters.discord import DiscordUpdater
from .updaters.github import GitHubUpdater
from .updaters.instagram import InstagramUpdater
from .updaters.spotify import SpotifyPlaylistUpdater
from .utils import print_error


class CountersProgram:
    """
    Encapsulation of main program. Runs the pipeline of steps to load
    the central JSON configuration file, prepare updaters, and run
    updaters, populating the provided failure log with any errors
    encountered.
    """

    def __init__(
        self,
        options: ProgramOptions,
        failure_log: FailureLog,
    ) -> None:
        self.options = options
        self.failure_log = failure_log

    def run(self) -> None:
        """Run the main process."""
        data = self._load_bio_config_json()
        if data is None:
            return

        driver = self._init_web_driver()
        if driver is None:
            return

        try:
            updaters = self._get_updaters(data, driver)
            self._run_updaters(updaters)
        finally:
            driver.quit()

    def _load_bio_config_json(self) -> dict | None:
        try:
            data = load_bio_config_json()
            print("JSON data loaded.")
            return data
        except Exception as exc:
            print("FAILED to load JSON data.")
            self.failure_log.json = exc
            return None

    def _init_web_driver(self) -> webdriver.Edge | None:
        try:
            if self.options.driver_path is None:
                driver_path = EdgeChromiumDriverManager().install()
            else:
                driver_path = str(self.options.driver_path)

            service = Service(executable_path=driver_path)
            options = Options()
            if not self.options.windowed:
                options.add_argument("--headless")

            driver = webdriver.Edge(service=service, options=options)
            driver.implicitly_wait(WAIT_TIMEOUT)
            driver.maximize_window()
            print("Driver initialized.")
            return driver

        except Exception as exc:
            print("FAILED to initialize driver.")
            self.failure_log.driver = exc
            return None

    def _get_updaters(
        self,
        data: dict,
        driver: webdriver.Edge,
    ) -> list[Updater]:
        updaters = list[Updater]()

        # The tasks for these platforms are self-contained.

        if self.options.run_discord:
            updaters.append(DiscordUpdater(data["discord"], driver))

        if self.options.run_instagram:
            updaters.append(InstagramUpdater(data["instagram"], driver))

        if self.options.run_github:
            updaters.append(GitHubUpdater(data["github"], driver))

        # Spotify is by playlist, and its key maps to a list of playlist
        # configuration objects.

        if self.options.run_spotify:
            for playlist_config in data["spotify"]:
                updater = SpotifyPlaylistUpdater(playlist_config, driver)
                updaters.append(updater)

        return updaters

    def _run_updaters(self, updaters: list[Updater]) -> None:
        if not updaters:
            print(
                "Nothing to update! "
                f"Check your configuration file at {JSON_FILE_PATH}."
            )
            return

        today = date.today()

        for updater in updaters:
            platform_name = updater.platform_name
            try:
                details = updater.prepare_details(today)
                updater.update_bio(details)
                print(f"Updated {platform_name}.")
            except Exception as exc:
                print_error(f"FAILED to update {platform_name}.")
                self.failure_log.platforms[platform_name] = exc
