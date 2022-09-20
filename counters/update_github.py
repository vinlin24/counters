"""update_github.py

Interface for updating the GitHub profile bio.
"""

from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.common.by import By

from .config import GITHUB_EMAIL, GITHUB_PASSWORD, GITHUB_PROFILE_URL
from .selectors.github import EMAIL_INPUT, PASSWORD_INPUT

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


# ==================== INTERFACE FUNCTION ==================== #


def update_profile_bio(driver: webdriver.Edge, bio: str | None) -> None:
    if bio is None:
        return

    # Start at the login page that redirects to my profile after login
    login_base_url = "https://github.com/login"
    param = urlencode({"return_to": GITHUB_PROFILE_URL})
    login_url = f"{login_base_url}?{param}"

    # Webscraping sequences
    driver.get(login_url)
    _login(driver)
