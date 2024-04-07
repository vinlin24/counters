"""discord.py

Interface for updating Discord custom status.
"""

from datetime import date
from typing import TypedDict

from rich.panel import Panel
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from ..config import DISCORD_EMAIL, DISCORD_PASSWORD, PLATFORM_DISCORD
# Experimenting CSS selectors as an alternative to full XPaths
# Not sure how often these will change in comparison
from ..selectors.discord import (AVATAR_ICON, EDIT_STATUS_ITEM, EMAIL_INPUT,
                                 PASSWORD_INPUT, SET_STATUS_ITEM, STATUS_INPUT)
from ..utils import format_generic_task_preview
from .base import Updater


class DiscordDetails(TypedDict):
    status: str | None


class DiscordUpdater(Updater[DiscordDetails]):
    @property
    def platform_name(self) -> str:
        return PLATFORM_DISCORD

    def prepare_details(self, today: date) -> DiscordDetails:
        # Fill placeholder in status template if provided.
        start: date | None = self.data["start"]
        status: str | None = self.data["status"]
        if start is not None and status is not None:
            status = status.format(self.day_number(start, today))

        return {"status": status}

    def update_bio(
        self,
        details: DiscordDetails,
        driver: webdriver.Edge,
    ) -> None:
        status = details["status"]
        if status is None:
            return
        driver.get("https://discord.com/login")
        self._login(driver)
        self._update_status(driver, status)

    def format_preview(self, details: DiscordDetails) -> Panel:
        return format_generic_task_preview(
            platform_name="Discord",
            body=details["status"],
            color="blue",
        )

    def _login(self, driver: webdriver.Edge) -> None:
        # Find elements
        email_input = driver.find_element(*EMAIL_INPUT)
        password_input = driver.find_element(*PASSWORD_INPUT)

        # Enter credentials
        email_input.clear()
        email_input.send_keys(DISCORD_EMAIL)
        password_input.clear()
        password_input.send_keys(DISCORD_PASSWORD + "\n")

    def _update_status(self, driver: webdriver.Edge, status: str) -> None:
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
