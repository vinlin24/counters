"""github.py

Interface for updating the GitHub profile bio.
"""

from datetime import date
from typing import TypedDict

from github import Auth, Github
from rich.panel import Panel

from ..bios import day_number
from ..config import GITHUB_PAT, PLATFORM_GITHUB
from ..updaters.base import Updater
from ..utils import format_generic_task_preview


class GitHubDetails(TypedDict):
    bio: str | None


class GitHubUpdater(Updater[GitHubDetails]):
    @property
    def platform_name(self) -> str:
        return PLATFORM_GITHUB

    def prepare_details(self, today: date) -> GitHubDetails:
        # Fill placeholder in bio template if provided.
        start: date | None = self.data["start"]
        bio: str | None = self.data["bio"]
        if start is not None and bio is not None:
            bio = bio.format(day_number(start, today))

        return {"bio": bio}

    def update_bio(self, details: GitHubDetails, _) -> None:
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
            body=details["bio"],
            color="white",
        )
