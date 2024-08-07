"""instagram.py

Defines CSS selectors for Selenium scraping of the Instagram web app.
Some of these values are still full xpaths, denoted with the `XPATH_`
prefix in their name, because I couldn't get CSS selectors to work.
"""

from .selector import CSSSelector, XPathSelector

USERNAME_INPUT = CSSSelector(
    "#loginForm > div > div:nth-child(1) > div > label > input")
"""Input text box for username on the login page."""

PASSWORD_INPUT = CSSSelector(
    "#loginForm > div > div:nth-child(2) > div > label > input")
"""Input text box for password on the login page."""

LOGIN_BUTTON = CSSSelector("#loginForm > div > div:nth-child(3) > button")
"""Login button on the login page."""

# As of 2024-02-11:
# CSS selector: #mount_0_0_cI > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y > section > main > div > div > div > div > div
# Full XPath: /html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div

NOT_NOW_BUTTON = XPathSelector(
    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div/div/div/div"
)
"""Button that appears as part of the "Save Your Login Info?" prompt.

For some reason, the CSS selector doesn't work, so I'm using the full
xpath.
"""

BIO_BOX = CSSSelector("#pepBio")
"""Input text area for updating the user bio."""

# As of 2024-02-11:
# CSS selector: #mount_0_0_ji > div > div > div.x9f619.x1n2onr6.x1ja2u2z > div > div > div.x78zum5.xdt5ytf.x1t2pt76.x1n2onr6.x1ja2u2z.x10cihs4 > div.x9f619.xvbhtw8.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1qughib > div.x1gryazu.xh8yej3.x10o80wk.x14k21rp.x17snn68.x6osk4m.x1porb0y > section > main > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div > form > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.xuk3077.x1oa3qoh.x1nhvcw1 > div
# Full XPath: /html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[3]/div/div/form/div[4]/div

SUBMIT_BUTTON = XPathSelector(
    "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/section/main/div/div[3]/div/div/form/div[4]/div"
)
"""Submit button on the "Edit profile" page.

Note that you should make an edit first to change the submit button
state from grayed out to active before checking what selector to use.
"""

PROFILE_SAVED = XPathSelector("/html/body/div[3]/div[1]/div/div/div/p")
"""Flash notification that appears after submitting a bio update.

For some reason, the CSS selector doesn't work, so I'm using the same
full xpath from before.
"""
