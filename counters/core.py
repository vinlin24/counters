# pylint: disable=broad-exception-caught

from datetime import date

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from .config import EXIT_FAILURE, JSON_FILE_PATH, WAIT_TIMEOUT, ProgramOptions
from .dry_run import execute_dry_run
from .emailer import send_email
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

    def __init__(self, options: ProgramOptions) -> None:
        self.options = options
        self.failure_log = FailureLog()

    def run(self) -> int:
        """Run the main process and return the exit code to use."""
        data = self._load_bio_config_json()
        if data is None:
            return EXIT_FAILURE

        updaters = self._get_updaters(data)

        if self.options.dry_run_date is not None:
            return execute_dry_run(
                updaters,
                self.options.dry_run_date,
                self.options.dry_run_one_per_line,
            )

        driver = self._init_web_driver()
        if driver is None:
            return EXIT_FAILURE

        self._run_updaters(updaters, driver)
        driver.quit()

        self._write_failure_report(updaters)
        return self.failure_log.get_exit_code()

    def _load_bio_config_json(self) -> dict | None:
        try:
            return load_bio_config_json()
        except Exception as exc:
            print_error("FAILED to load JSON data.")
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
            print_error("FAILED to initialize driver.")
            self.failure_log.driver = exc
            return None

    def _get_updaters(self, data: dict) -> list[Updater]:
        updaters = list[Updater]()

        # The tasks for these platforms are self-contained.

        if self.options.run_discord:
            updaters.append(DiscordUpdater(data["discord"]))

        if self.options.run_instagram:
            updaters.append(InstagramUpdater(data["instagram"]))

        if self.options.run_github:
            updaters.append(GitHubUpdater(data["github"]))

        # Spotify is by playlist, and its key maps to a list of playlist
        # configuration objects.

        if self.options.run_spotify:
            for playlist_config in data["spotify"]:
                updater = SpotifyPlaylistUpdater(playlist_config)
                updaters.append(updater)

        return updaters

    def _run_updaters(
        self,
        updaters: list[Updater],
        driver: webdriver.Edge,
    ) -> None:
        if not updaters:
            print(
                "Nothing to update! "
                f"Check your configuration file at {JSON_FILE_PATH}."
            )
            return

        date_to_update_to = self.options.date_to_update_to

        for updater in updaters:
            platform_name = updater.platform_name
            try:
                details = updater.prepare_details(date_to_update_to)
                updater.update_bio(details, driver)
                print(f"Updated {platform_name}.")
            except Exception as exc:
                print_error(f"FAILED to update {platform_name}.")
                self.failure_log.platforms[platform_name] = exc

    def _write_failure_report(self, updaters: list[Updater]) -> None:
        if not self.options.console_only:
            platforms_attempted = [u.platform_name for u in updaters]
            report = self.failure_log.generate_report(platforms_attempted)
            self.failure_log.write_report_to_file(report)
            send_email(report)
        else:
            self.failure_log.print_tracebacks()
