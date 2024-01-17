"""__init__.py

Package initialization.
"""

import os


def ensure_file_path(file_path: str) -> None:
    """Helper function for ensuring the existence of a file.

    Args:
        file_path (str): Absolute path to the file to ensure the
        existence of. Must not be a directory.

    Precondition:
        Up to the file's grandparent must exist. In other words, the
        file and its enclosing directory are allowed to not exist, but
        no more than that.

    Postcondition:
        Does nothing if the file already exists. Otherwise, creates the
        file and its directory if necessary.
    """
    if not os.path.exists(file_path):
        # Attempt to make the directory if it exists
        try:
            os.mkdir(os.path.dirname(file_path))
        except FileExistsError:
            pass
        # Make the file
        with open(file_path, "w", encoding="utf-8"):
            pass
