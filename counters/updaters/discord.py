"""discord.py

Interface for updating Discord custom status.
"""

from datetime import date
from typing import TypedDict

from rich.panel import Panel
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from ..bios import day_number
from ..config import DISCORD_EMAIL, DISCORD_PASSWORD
# Experimenting CSS selectors as an alternative to full XPaths
# Not sure how often these will change in comparison
from ..selectors.discord import (AVATAR_ICON, EDIT_STATUS_ITEM, EMAIL_INPUT,
                                 PASSWORD_INPUT, SET_STATUS_ITEM, STATUS_INPUT)
from ..updaters.base import Updater
from ..utils import format_generic_task_preview


class DiscordDetails(TypedDict):
    status: str | None


class DiscordUpdater(Updater[DiscordDetails]):
    def prepare_details(self, today: date) -> DiscordDetails:
        task: dict = self.data["discord"]

        # Fill placeholder in status template if provided.
        start: date | None = task["start"]
        status: str | None = task["status"]
        if start is not None and status is not None:
            status = status.format(day_number(start, today))

        return {"status": status}

    def update_bio(self, details: DiscordDetails) -> None:
        status = details["status"]
        if status is None:
            return
        self.driver.get("https://discord.com/login")
        self._login()
        self._update_status(status)

    def format_preview(self, details: DiscordDetails) -> Panel:
        return format_generic_task_preview(
            platform_name="Discord",
            body_text=details["status"],
            color="blue",
        )

    def _login(self) -> None:
        # Find elements
        email_input = self.driver.find_element(*EMAIL_INPUT)
        password_input = self.driver.find_element(*PASSWORD_INPUT)

        # Enter credentials
        email_input.clear()
        email_input.send_keys(DISCORD_EMAIL)
        password_input.clear()
        password_input.send_keys(DISCORD_PASSWORD + "\n")

    def _update_status(self, status: str) -> None:
        # Bring up menu in the bottom left corner
        avatar_icon = self.driver.find_element(*AVATAR_ICON)
        avatar_icon.click()

        # Click the "Edit custom status" option
        # If there's currently no status, it's "Set custom status" instead
        try:
            custom_status = self.driver.find_element(*EDIT_STATUS_ITEM)
        except NoSuchElementException:
            custom_status = self.driver.find_element(*SET_STATUS_ITEM)
        custom_status.click()

        # Get the input text bot
        status_input = self.driver.find_element(*STATUS_INPUT)

        # Enter the status into the text box
        status_input.clear()
        status_input.send_keys(status + "\n")


# TODO: Replace below when finished refactoring other modules.
# ==================== SCRAPING SUBROUTINES ==================== #


def _login(driver: webdriver.Edge) -> None:
    """Handle authentication landing page.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
    """
    # Find elements
    email_input = driver.find_element(*EMAIL_INPUT)
    password_input = driver.find_element(*PASSWORD_INPUT)

    # Enter credentials
    email_input.clear()
    email_input.send_keys(DISCORD_EMAIL)
    password_input.clear()
    password_input.send_keys(DISCORD_PASSWORD + "\n")


def _update_status(driver: webdriver.Edge, status: str) -> None:
    """Handle navigating to the input box and submitting new status.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
        status (str): Status to input as the new custom status.
    """
    # Bring up menu in the bottom left corner
    avatar_icon = driver.find_element(*AVATAR_ICON)
    avatar_icon.click()

    # Click the "Edit custom status" option
    # If there's currently no status, it's "Set custom status" instead
    try:
        custom_status = driver.find_element(*EDIT_STATUS_ITEM)
    except NoSuchElementException:
        custom_status = driver.find_element(*SET_STATUS_ITEM)
    custom_status.click()

    # Get the input text bot
    status_input = driver.find_element(*STATUS_INPUT)

    # Enter the status into the text box
    status_input.clear()
    status_input.send_keys(status + "\n")


# ==================== INTERFACE FUNCTION ==================== #


def update_status(driver: webdriver.Edge, status: str | None) -> None:
    """Update Discord custom status with new status.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
        status (str | None, optional): New custom status. Defaults to
        None, meaning leave the status unchanged, in which case, this
        function does nothing.
    """
    if status is None:
        return

    # Webscraping sequences
    driver.get("https://discord.com/login")
    _login(driver)
    _update_status(driver, status)
