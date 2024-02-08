"""discord.py

Defines CSS selectors for Selenium scraping of the Discord web app.
"""

EMAIL_INPUT = "#uid_7"
"""The text input box for email on the login page."""

PASSWORD_INPUT = "#uid_9"
"""The text input box for password on the login page."""

AVATAR_ICON = "#app-mount > div.appAsidePanelWrapper__714a6 > div.notAppAsidePanel__9d124 > div.app_b1f720 > div > div.layers__1c917.layers_a23c37 > div > div > div > div > div > section > div.container_ca50b9 > div.avatarWrapper_ba5175.withTagAsButton_cc125f > div.wrapper_edb6e0.avatar_f8541f"
"""The circular, clickable avatar icon in the bottom left."""

SET_STATUS_ITEM = "#account-set-custom-status"
"""The "Set Custom Status" menu item in the avatar menu popup."""

EDIT_STATUS_ITEM = "#account-edit-custom-status"
"""The "Edit Custom Status" menu item in the avatar menu popup."""

STATUS_INPUT = ".inputDefault__80165"
"""The text input box that appear upon clicking Edit Custom Status."""

EMOJI_IMG = "#app-mount > div.appAsidePanelWrapper__714a6 > div.notAppAsidePanel__9d124 > div.app_b1f720 > div > div.layers__1c917.layers_a23c37 > div > div > div > div > div > section > div.container_ca50b9 > div.avatarWrapper_ba5175.withTagAsButton_cc125f > div.nameTag__0e320.canCopy__81263 > div.panelSubtextContainer_f28bed > div > div > div.default_cae228 > div > img"
"""The <img> of the emoji part, if included."""

TEXT_SPAN = "#app-mount > div.appAsidePanelWrapper__714a6 > div.notAppAsidePanel__9d124 > div.app_b1f720 > div > div.layers__1c917.layers_a23c37 > div > div > div > div > div > section > div.container_ca50b9 > div.avatarWrapper_ba5175.withTagAsButton_cc125f > div.nameTag__0e320.canCopy__81263 > div.panelSubtextContainer_f28bed > div > div > div.default_cae228 > div > span"
"""The <span> of the text part, if included."""
