"""instagram.py

Interface for updating Instagram bio.
"""

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from ..config import INSTAGRAM_PASSWORD, INSTAGRAM_USERNAME
from ..selectors.instagram import (BIO_BOX, LOGIN_BUTTON, NOT_NOW_BUTTON,
                                   PASSWORD_INPUT, SUBMIT_BUTTON,
                                   USERNAME_INPUT)


def _login(driver: webdriver.Edge) -> None:
    """Handle the authentication landing page.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
    """
    # Find elements
    username_elem = driver.find_element(*USERNAME_INPUT)
    password_elem = driver.find_element(*PASSWORD_INPUT)
    login_button = driver.find_element(*LOGIN_BUTTON)

    # Input credentials and login
    username_elem.clear()
    username_elem.send_keys(INSTAGRAM_USERNAME)
    password_elem.clear()
    password_elem.send_keys(INSTAGRAM_PASSWORD)
    login_button.click()


def _navigate_to_profile(driver: webdriver.Edge) -> None:
    """Handle navigating to the profile edit page after authenticated.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
    """
    # Dismiss the "Save login info" if it appears
    condition = EC.presence_of_element_located(
        (NOT_NOW_BUTTON.by, NOT_NOW_BUTTON.value)
    )
    try:
        not_now_button: WebElement = WebDriverWait(driver, 5).until(condition)
        not_now_button.click()
    except TimeoutException:
        # Just try to redirect again bro sigh
        driver.get("https://www.instagram.com/accounts/edit")


def _update_profile(driver: webdriver.Edge, bio: str) -> None:
    """Handle updating the bio after reaching the edit profile page.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
        bio (str): Bio to input as the new bio.

    Raises:
        TimeoutException: Couldn't locate a certain element within
        `WAIT_TIMEOUT` seconds.
    """
    # Find elements
    bio_box = driver.find_element(*BIO_BOX)

    # Submit new bio string
    bio_box.clear()
    bio_box.send_keys(bio)

    # NOTE: If you don't edit anything, the button will be disabled
    submit_button = driver.find_element(*SUBMIT_BUTTON)
    submit_button.click()

    # Make sure the update registered
    # try:
    #     WebDriverWait(driver, WAIT_TIMEOUT).until(
    #         EC.presence_of_element_located((By.XPATH, XPATH_PROFILE_SAVED))
    #     )
    # except TimeoutException:
    #     print("Couldn't locate 'Profile saved' flash notification.")
    #     log.error("Couldn't locate 'Profile saved' flash notification.")
    #     raise


def update_bio(driver: webdriver.Edge, bio: str | None = None) -> None:
    """Update Instagram profile bio with new bio.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
        bio (str | None, optional): New bio. Defaults to None, meaning
        leave the bio unchanged, in which case, this function does
        nothing.
    """
    if bio is None:
        return

    # Webscraping sequences
    driver.get("https://www.instagram.com/accounts/edit")
    _login(driver)
    _navigate_to_profile(driver)
    _update_profile(driver, bio)
