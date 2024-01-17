"""core.py

Webscraping sequences to obtain the current Discord cusom status.
"""

from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from ..config import DISCORD_EMAIL, DISCORD_PASSWORD
from ..selectors.discord import (EMAIL_INPUT, EMOJI_IMG, PASSWORD_INPUT,
                                 TEXT_SPAN)
from .driver import get_driver
from .logger import log_exit_status, send_error_email
from .writer import log_status

# ==================== SCRAPING SUBROUTINES ==================== #


def _login(driver: webdriver.Edge) -> None:
    """Handle authentication landing page.

    Copied directly from my counters/update_discord.py.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
    """
    # Find elements
    email_input = driver.find_element(By.CSS_SELECTOR, EMAIL_INPUT)
    password_input = driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT)

    # Enter credentials
    email_input.clear()
    email_input.send_keys(DISCORD_EMAIL)
    password_input.clear()
    password_input.send_keys(DISCORD_PASSWORD + "\n")


def _extract_emoji(driver: webdriver.Edge) -> str | None:
    """Extract the emoji part of the custom status."""
    # An emoji was used: this img element should be present
    try:
        emoji_img = driver.find_element(By.CSS_SELECTOR, EMOJI_IMG)
    # An emoji wasn't used
    except NoSuchElementException:
        return None

    return emoji_img.get_attribute("alt")


def _extract_text(driver: webdriver.Edge) -> str:
    """Extract the text part of the custom status."""
    # Get the <span> element that contains the text part
    try:
        text_span = driver.find_element(By.CSS_SELECTOR, TEXT_SPAN)
    # <span> element doesn't exist if text is blank
    except NoSuchElementException:
        return ""

    return text_span.text


def _get_status(driver: webdriver.Edge) -> tuple[str | None, str]:
    """Extract the current Discord custom status.

    Args:
        driver (webdriver.Edge): Initialized web driver instance.

    Returns:
        tuple[str | None, str]: A 2-tuple containing:
            0: The emoji part as a Unicode character
            1: The text part.
    """
    # Scraping sequences here
    driver.get("https://discord.com/login")
    _login(driver)
    emoji = _extract_emoji(driver)
    text = _extract_text(driver)
    return (emoji, text)


# ==================== INTERFACE FUNCTION ==================== #


def run_status_logger(console_only: bool,
                      headless: bool,
                      driver_path: Path | None = None,
                      ) -> bool:
    try:
        with get_driver(headless, driver_path) as driver:
            emoji, text = _get_status(driver)
        print(f"Extracted {emoji=} and {text=}.")
        # I almost never not have a status; this must mean scraping failed
        if not emoji and not text:
            # UPDATE: At least try to log something so the log file
            # looks consistent (no missing dates).
            log_status(
                emoji=None, text="[ no status set or failed to extract ]")
            raise Exception(
                "Status could not be extracted. If you really did not have a "
                "status set up for today, ignore this. It is also possible "
                "that the page did not load in time. Check your connection."
            )
    except Exception as e:
        if not console_only:
            log_exit_status(e)
            send_error_email(e)
        print("Finished running the status-logger package: ERROR.")
        print(f"{type(e).__name__}: {e}")
        return False
    else:
        if not console_only:
            log_status(emoji, text)
            log_exit_status(None)
        print("Finished running the status-logger package: SUCCESS.")
        return True
