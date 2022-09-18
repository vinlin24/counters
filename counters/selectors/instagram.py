"""instagram.py

Defines CSS selectors for Selenium scraping of the Instagram web app.
Some of these values are still full xpaths, denoted with the `XPATH_`
prefix in their name, because I couldn't get CSS selectors to work.
"""

USERNAME_INPUT = "#loginForm > div > div:nth-child(1) > div > label > input"
"""Input text box for username on the login page."""

PASSWORD_INPUT = "#loginForm > div > div:nth-child(2) > div > label > input"
"""Input text box for password on the login page."""

LOGIN_BUTTON = "#loginForm > div > div:nth-child(3) > button"
"""Login button on the login page."""

XPATH_NOT_NOW_BUTTON = "/html/body/div[1]/section/main/div/div/div/div/button"
"""Button that appears as part of the "Save Your Login Info?" prompt.

For some reason, the CSS selector doesn't work, so I'm using the same
full xpath from before.
"""

BIO_BOX = "#pepBio"
"""Input text area for updating the user bio."""

SUBMIT_BUTTON = "._acan._acap._acas"
"""Submit button on the "Edit profile" page."""

XPATH_PROFILE_SAVED = "/html/body/div[3]/div[1]/div/div/div/p"
"""Flash notification that appears after submitting a bio update.

For some reason, the CSS selector doesn't work, so I'm using the same
full xpath from before.
"""
