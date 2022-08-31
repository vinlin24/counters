"""update_discord.py

Interface for updating Discord custom status.
"""

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

from .config import (DISCORD_EMAIL, DISCORD_PASSWORD, EDGE_DRIVER_PATH,
                     WAIT_TIMEOUT)

# ==================== FULL XPATHS ==================== #
# These risk changing every damn update :/

XPATH_LOGIN_BUTTON = ("/html/body/div[1]/div/div/div[1]/div[1]/header[1]/nav/"
                      "div/a")
XPATH_EMAIL_INPUT = ("/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/"
                     "form/div/div/div[1]/div[2]/div[1]/div/div[2]/input")
XPATH_PASSWORD_INPUT = ("/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/"
                        "form/div/div/div[1]/div[2]/div[2]/div/input")
XPATH_AVATAR_ICON = ("/html/body/div[1]/div[2]/div/div[1]/div/div[2]/div/"
                     "div[1]/div/div/div[1]/section/div[2]/div[1]/div[1]")
XPATH_CUSTOM_STATUS = ("/html/body/div[1]/div[2]/div/div[3]/div/div/div/div/"
                       "div[3]/div[2]")
XPATH_STATUS_INPUT = ("/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div/"
                      "div[2]/div[1]/div[2]/div/div[2]/input")


# ==================== SCRAPING SUBROUTINES ==================== #

def _login(driver: webdriver.Edge) -> None:
    """Handle authentication landing page.

    Args:
        driver (webdriver.Edge): Edge web driver instance.
    """
    # Find elements
    email_input = driver.find_element(
        "xpath",
        XPATH_EMAIL_INPUT
    )
    password_input = driver.find_element(
        "xpath",
        XPATH_PASSWORD_INPUT
    )

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
    avatar_icon = driver.find_element(
        "xpath",
        XPATH_AVATAR_ICON
    )
    avatar_icon.click()

    # Click the "Edit custom status" option
    custom_status = driver.find_element(
        "xpath",
        XPATH_CUSTOM_STATUS
    )
    custom_status.click()

    # Get the input text bot
    status_input = driver.find_element(
        "xpath",
        XPATH_STATUS_INPUT
    )

    # Enter the status into the text box
    status_input.clear()
    status_input.send_keys(status + "\n")


# ==================== INTERFACE FUNCTION ==================== #


def update_status(status: str | None) -> None:
    """Update Discord custom status with new status.

    Args:
        status (str | None, optional): New custom status. Defaults to
        None, meaning leave the status unchanged, in which case, this
        function does nothing.
    """
    if status is None:
        return

    # Initialize driver
    service = Service(str(EDGE_DRIVER_PATH))
    options = Options()
    options.headless = True
    # Headless option by default causes window to be tiny, which interferes
    # with finding elements if it's rendered responsively
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Edge(service=service, options=options)

    # Wait for page to load
    driver.get("https://discord.com/login")
    driver.implicitly_wait(WAIT_TIMEOUT)

    # Webscraping sequences
    _login(driver)
    _update_status(driver, status)

    # Cleanup
    driver.quit()
