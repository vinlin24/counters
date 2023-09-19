"""bios.py

Defines functions that load the central JSON file, fill placeholders,
and prepare the arguments to pass to their respective update handlers.
"""

import json
from datetime import date, datetime
from typing import Literal

import jsonschema

from .config import DATE_FORMAT, JSON_FILE_PATH, JSON_SCHEMA_PATH


def day_number(start: date) -> int:
    """Calculate the day number of today relative to a starting date.

    Args:
        start (date): The date considered to be "Day 1."

    Returns:
        int: Day number since the starting date.
    """
    # +1 to start at Day 1
    return (date.today() - start).days + 1


def _convert_start_date(d: dict[str, str | None]) -> None:
    """Convert the value of the "start" key to a date object.

    Does nothing if the value is None.

    Args:
        d (dict[str, str | None]): The mapping containing the
        "start" key.
    """
    date_string = d["start"]
    if date_string is None:
        return
    dt = datetime.strptime(date_string, DATE_FORMAT)
    d["start"] = dt.date()  # type: ignore


def _validate_json() -> dict:
    """Validate the JSON to load, returning it if successful.

    Raises:
        jsonschema.ValidationError: If the JSON to load is invalid.
        jsonschema.SchemaError: If the schema itself is invalid.

    Returns:
        dict: The JSON data if validated successfully.
    """
    with JSON_SCHEMA_PATH.open("rt", encoding="utf-8") as fp:
        schema = json.load(fp)
    with JSON_FILE_PATH.open("rt", encoding="utf-8") as fp:
        data = json.load(fp)

    jsonschema.validate(instance=data, schema=schema)
    return data


LoadedDict = dict[Literal["discord", "instagram", "spotify"],
                  dict[str, str | None] |
                  list[dict[str, str | None | date]]]


def load_json() -> LoadedDict:
    """Load and parse the central JSON file containing bio details.

    Raises:
        ValueError: A violation of the JSON schema where the keys map
        to something other than a list or a dict.

    Returns:
        LoadedDict: The loaded data. Start dates are converted from str
        to datetime.date objects.
    """
    # Validate first
    data = _validate_json()

    # Postprocessing: convert "start" values to date objects in-place
    for key, val in data.items():
        # Optional $schema key
        if key == "$schema":
            continue
        # Task objects
        if isinstance(val, dict):
            _convert_start_date(val)
        # List of task objects
        elif isinstance(val, list):
            for entry in val:
                _convert_start_date(entry)

    return data


def get_discord_task(data: LoadedDict) -> str | None:
    """Prepare the "status" argument to pass to update_status().

    Args:
        data (LoadedDict): The loaded and configured data from the
        central JSON file.

    Returns:
        str | None: The instantiated status template to pass to
        update_status(), or None if opted out of updating status.
    """
    # Extract Discord part
    task: dict = data["discord"]  # type: ignore

    # Fill placeholder in status template if provided
    start: date | None = task["start"]
    status: str | None = task["status"]
    if start is not None and status is not None:
        status = status.format(day_number(start))

    return status


def get_instagram_task(data: LoadedDict) -> str | None:
    """Prepare the "bio" argument to pass to update_bio().

    Args:
        data (LoadedDict): The loaded and configured data from the
        central JSON file.

    Returns:
        str | None: The instantiated bio template to pass to
        update_bio(), or None if opted out of updating bio.
    """
    # Extract Instagram part
    task: dict = data["instagram"]  # type: ignore

    # Fill placeholder in bio template if provided
    start: date | None = task["start"]
    bio: str | None = task["bio"]
    if start is not None and bio is not None:
        bio = bio.format(day_number(start))

    return bio


def get_spotify_tasks(data: LoadedDict) -> list[dict[str, str | None]]:
    """Prepare the keyword arguments to pass to update_playlist().

    Args:
        data (LoadedDict): The loaded and configured data from the
        central JSON file.

    Returns:
        list[dict[str, str | None]]: A list of entries, each of which
        being a set of keyword arguments to pass to update_playlist()
        for that specific playlist task.
    """
    # Extract Spotify part
    tasks: list = data["spotify"]  # type: ignore

    result = []
    for task in tasks:
        # Fill day number placeholders if included
        name: str | None = task["name"]
        description: str | None = task["description"]
        start: date | None = task["start"]
        comment: str | None = task["comment"]
        if start is not None:
            if name is not None:
                name = name.format(day_number(start))
            if description is not None:
                description = description.format(day_number(start))

        # Prepare the kwargs for this task
        kwargs = {
            "playlist_id": task["playlist_id"],
            "name": name,
            "description": description,
            "comment": comment,
        }
        result.append(kwargs)

    return result


def get_github_task(data: LoadedDict) -> str | None:
    """Prepare the "bio" argument to pass to update_profile_bio().

    Args:
        data (LoadedDict): The loaded and configured data from the
        central JSON file.

    Returns:
        str | None: The instantiated bio template to pass to
        update_profile_bio(), or None if opted out of updating bio.
    """
    # Extract GitHub part
    task: dict = data["github"]  # type: ignore

    # Fill placeholder in bio template if provided
    start: date | None = task["start"]
    bio: str | None = task["bio"]
    if start is not None and bio is not None:
        bio = bio.format(day_number(start))

    return bio
