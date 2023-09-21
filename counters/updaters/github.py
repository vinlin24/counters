"""github.py

Interface for updating the GitHub profile bio.
"""

from github import Auth, Github

from ..config import GITHUB_PAT

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
