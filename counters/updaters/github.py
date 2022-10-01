"""github.py

Interface for updating the GitHub profile bio.
"""

from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.common.by import By

from ..config import GITHUB_EMAIL, GITHUB_PASSWORD, GITHUB_PROFILE_URL
from ..selectors.github import (BIO_TEXTAREA, EDIT_PROFILE_BUTTON, EMAIL_INPUT,
                                PASSWORD_INPUT, SAVE_BUTTON)

# ==================== SCRAPING SUBROUTINES ==================== #


def _login(driver: webdriver.Edge) -> None:
    """Handle authentication landing page.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
    """
    # Find elements
    email_input = driver.find_element(By.CSS_SELECTOR, EMAIL_INPUT)
    password_input = driver.find_element(By.CSS_SELECTOR, PASSWORD_INPUT)

    # Enter credentials
    email_input.clear()
    email_input.send_keys(GITHUB_EMAIL)
    password_input.clear()
    password_input.send_keys(GITHUB_PASSWORD + "\n")


def _update_bio(driver: webdriver.Edge, bio: str) -> None:
    # Enter edit profile mode
    edit_button = driver.find_element(By.CSS_SELECTOR, EDIT_PROFILE_BUTTON)
    edit_button.click()

    # Edit the bio content
    bio_box = driver.find_element(By.CSS_SELECTOR, BIO_TEXTAREA)
    bio_box.clear()
    bio_box.send_keys(bio)

    # Save the changes
    save_button = driver.find_element(By.CSS_SELECTOR, SAVE_BUTTON)
    save_button.click()


# ==================== INTERFACE FUNCTION ==================== #


def update_profile_bio(driver: webdriver.Edge, bio: str | None) -> None:
    """Update GitHub profile bio with new text.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
        status (str | None, optional): New bio text. Defaults to None,
        meaning leave the status unchanged, in which case, this
        function does nothing.
    """
    if bio is None:
        return

    # Start at the login page that redirects to my profile after login
    login_base_url = "https://github.com/login"
    param = urlencode({"return_to": GITHUB_PROFILE_URL})
    login_url = f"{login_base_url}?{param}"

    # Webscraping sequences
    driver.get(login_url)
    _login(driver)
    _update_bio(driver, bio)
