"""github.py

Interface for updating the GitHub profile bio.
"""

from datetime import date
from typing import TypedDict

from github import Auth, Github
from rich.panel import Panel

from ..bios import day_number
from ..config import GITHUB_PAT
from ..updaters.base import Updater
from ..utils import format_generic_task_preview


class GitHubDetails(TypedDict):
    bio: str | None


class GitHubUpdater(Updater[GitHubDetails]):
    def prepare_details(self, today: date) -> GitHubDetails:
        task: dict = self.data["github"]

        # Fill placeholder in bio template if provided
        start: date | None = task["start"]
        bio: str | None = task["bio"]
        if start is not None and bio is not None:
            bio = bio.format(day_number(start, today))

        return {"bio": bio}

    def update_bio(self, details: GitHubDetails) -> None:
        bio = details["bio"]
        if bio is None:
            return
        auth = Auth.Token(GITHUB_PAT)
        github = Github(auth=auth)
        user = github.get_user()
        user.edit(bio=bio)

    def format_preview(self, details: GitHubDetails) -> Panel:
        return format_generic_task_preview(
            platform_name="GitHub",
            body_text=details["bio"],
            color="white",
        )


# TODO: Replace below when finished refactoring other modules.
# ==================== INTERFACE FUNCTION ==================== #


def update_profile_bio(bio: str | None) -> None:
    """Update GitHub profile bio with new text.

    Args:
        status (str | None, optional): New bio text. Defaults to None,
        meaning leave the status unchanged, in which case, this function
        does nothing.
    """
    if bio is None:
        return
    auth = Auth.Token(GITHUB_PAT)
    github = Github(auth=auth)
    user = github.get_user()
    user.edit(bio=bio)
