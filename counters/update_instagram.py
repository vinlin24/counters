"""update_instagram.py

Interface for updating Instagram bio.
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

from .config import (EDGE_DRIVER_PATH, INSTAGRAM_PASSWORD, INSTAGRAM_USERNAME,
                     WAIT_TIMEOUT)


def _login(driver: webdriver.Edge) -> None:
    """Handle the authentication landing page.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
    """
    # Find elements
    username_elem = driver.find_element(
        "xpath",
        "//*[@id=\"loginForm\"]/div/div[1]/div/label/input"
    )
    password_elem = driver.find_element(
        "xpath",
        "//*[@id=\"loginForm\"]/div/div[2]/div/label/input"
    )
    login_button = driver.find_element(
        "xpath",
        "//*[@id=\"loginForm\"]/div/div[3]/button/div"
    )

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
    # Dismiss the "Save login info"
    not_now_button = driver.find_element(
        "xpath",
        "/html/body/div[1]/section/main/div/div/div/div/button"
    )
    not_now_button.click()

    # Just redirect lol, not dealing with more popup shit
    driver.get("https://www.instagram.com/accounts/edit/")


def _update_profile(driver: webdriver.Edge, bio: str) -> None:
    """Handle updating the bio after reaching the edit profile page.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
        bio (str): Bio to input as the new bio.
    """
    # Find elements
    bio_box = driver.find_element(
        "xpath",
        "//*[@id=\"pepBio\"]"
    )
    submit_button = driver.find_element(
        "xpath",
        ("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/"
         "section/main/div/article/form/div[10]/div/div/button")
    )

    # Submit new bio string
    bio_box.clear()
    bio_box.send_keys(bio)
    submit_button.click()


def update_bio(bio: str | None = None) -> None:
    """Update Instagram profile bio with new bio.

    Args:
        bio (str | None, optional): New bio. Defaults to None, meaning
        leave the bio unchanged, in which case, this function does
        nothing.
    """
    if bio is None:
        return

    # Initialize driver
    service = Service(str(EDGE_DRIVER_PATH))
    options = Options()
    options.headless = False
    driver = webdriver.Edge(service=service, options=options)

    # Wait for page to load
    driver.get("https://www.instagram.com/direct/inbox/")
    driver.implicitly_wait(WAIT_TIMEOUT)

    # Webscraping sequences
    _login(driver)
    _navigate_to_profile(driver)
    _update_profile(driver, bio)

    # Cleanup
    driver.quit()
