"""github.py

Defines CSS selectors for Selenium scraping of the GitHub web app.
"""

EMAIL_INPUT = "#login_field"
"""The <input> email on the login page."""

PASSWORD_INPUT = "#password"
"""The <input> for password on the login page."""

EDIT_PROFILE_BUTTON = "div[class=\"Layout-sidebar\"] button[name=\"button\"][type=\"button\"]"
"""The edit profile <button> on the sidebar."""

BIO_TEXTAREA = "#user_profile_bio"
"""The Bio <textarea> when editing the profile."""

SAVE_BUTTON = "button[type=\"submit\"][class=\"btn-primary btn-sm btn\"]"
"""The Save <button> at the bottom of the sidebar."""
