#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mini version of my main `counters` program. This version only supports
the platforms that do not require Selenium i.e. those that have an
official web API to make requests to. At the moment, those are:

    - Spotify
    - GitHub
"""

# pylint: disable=missing-class-docstring,missing-function-docstring

import argparse
import functools
import json
import os
import sys
import traceback
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable, NoReturn, TypedDict

import dotenv
import github
import jsonschema
import tekore


class SpotifyPlaylistConfig(TypedDict):
    comment: str | None
    playlist_id: str
    name: str | None
    description: str | None
    start: str | None


class GitHubConfig(TypedDict):
    bio: str | None
    start: str | None


class BiosConfig(TypedDict):
    spotify: list[SpotifyPlaylistConfig]
    github: GitHubConfig


print_error = functools.partial(print, file=sys.stderr)


def load_bios_config(config_path: Path, schema_path: Path) -> BiosConfig:
    """Validate the JSON to load, returning it if successful.

    Raises:
        jsonschema.ValidationError: If the JSON to load is invalid.
        jsonschema.SchemaError: If the schema itself is invalid.

    Returns:
        BiosConfig: The JSON data if validated successfully.
    """
    with config_path.open("rt", encoding="utf-8") as config_file:
        data = json.load(config_file)
    with schema_path.open("rt", encoding="utf-8") as schema_file:
        schema = json.load(schema_file)

    jsonschema.validate(instance=data, schema=schema)
    return data


def day_number(start: date, today: date | None = None) -> int:
    """
    Calculate the day number of a date (default today) relative to a
    starting date. The actual heart of this program lol.

    Args:
        start (date): The date considered to be "Day 1."
        today: (date | None, optional): The date to consider "today".
        Defaults to today.

    Returns:
        int: Day number since the starting date.
    """
    today = today or date.today()
    # +1 to start at Day 1.
    return (today - start).days + 1


def resolve_iso_date_string(date_string: str) -> date:
    return datetime.strptime(date_string, "%Y-%m-%d").date()


def format_error(error: Exception) -> str:
    """Return the traceback of the error as a string.

    Postcondition:
        Adds an extra newline for padding.
    """
    return "".join(traceback.format_exception(error)) + "\n"


def dump_and_exit(errors: Iterable[Exception]) -> NoReturn:
    any_error = False
    for error in errors:
        formatted_error = format_error(error)
        print_error(formatted_error, file=sys.stderr)
        any_error = True
    sys.exit(1 if any_error else 0)


class GitHubUpdater:
    def __init__(self, config: GitHubConfig, client: github.Github) -> None:
        self.config = config
        self.client = client

    def update(self, today: date) -> None:
        bio = self.resolve_bio(today)
        if bio is None:
            return
        user = self.client.get_user()
        user.edit(bio=bio)

    def resolve_bio(self, today: date) -> str | None:
        start = self.config["start"]
        bio = self.config["bio"]
        if start is not None and bio is not None:
            start_date = resolve_iso_date_string(start)
            bio = bio.format(day_number(start_date, today))
        return bio


class SpotifyPlaylistUpdater:
    def __init__(
        self,
        config: SpotifyPlaylistConfig,
        client: tekore.Spotify,
    ) -> None:
        self.config = config
        self.client = client

    def update(self, today: date) -> None:
        playlist_id = self.config["playlist_id"]
        resolved_description = self.resolve_description(today)
        resolved_name = self.resolve_name(today)

        self.client.playlist_change_details(
            playlist_id=playlist_id,
            name=resolved_name,  # type: ignore
            description=resolved_description,  # type: ignore
        )

    def resolve_description(self, today: date) -> str | None:
        day_num = self.__get_day_num(today)
        description = self.config["description"]
        if day_num is None or description is None:
            return None
        return description.format(day_num)

    def resolve_name(self, today: date) -> str | None:
        day_num = self.__get_day_num(today)
        name = self.config["name"]
        if day_num is None or name is None:
            return None
        return name.format(day_num)

    def __get_day_num(self, today: date) -> int | None:
        start = self.config["start"]
        if start is None:
            return None
        start_date = resolve_iso_date_string(start)
        return day_number(start_date, today)


def valid_date(value: str) -> date:
    """
    Transform `value` into a date if possible, else raise
    `argparse.ArgumentTypeError`.

    Currently recognized date formats are ISO 8601 and certain
    convenience literals e.g. `"tomorrow"`.
    """
    value = value.strip().lower()

    # First try special literals.
    if value in ("tomorrow", "tmrw", "tmr"):
        tomorrow = date.today() + timedelta(days=1)
        return tomorrow
    if value in ("today", "now"):
        return date.today()

    # Then try ISO 8601.
    try:
        return resolve_iso_date_string(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"{value!r} is not a valid ISO date",
        ) from None


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
)
parser.add_argument(
    "date_to_update_to",
    metavar="DATE",
    nargs="?",
    type=valid_date,
    default=date.today(),
    help="date to update counters to (defaults to today)",
)
parser.add_argument(
    "-c", "--config",
    dest="config_path",
    metavar="PATH",
    type=Path,
    required=True,
    help="path to configuration file",
)


class CountersProgram:
    def __init__(self, config: BiosConfig, today: date) -> None:
        self.config = config
        self.today = today

    def run_all(self) -> list[Exception]:
        return self.run_github() + self.run_spotify()

    def run_github(self) -> list[Exception]:
        try:
            auth = github.Auth.Token(os.environ["GITHUB_PAT"])
            client = github.Github(auth=auth)
            updater = GitHubUpdater(
                config=self.config["github"],
                client=client,
            )
        except Exception as error:
            print_error("FAILED to initialize GitHub.")
            return [error]

        try:
            updater.update(self.today)
        except Exception as error:
            print_error("FAILED to update GitHub.")
            return [error]

        print("Updated GitHub.")
        return []

    def run_spotify(self) -> list[Exception]:
        try:
            token = tekore.refresh_user_token(
                client_id=os.environ["SPOTIFY_CLIENT_ID"],
                client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
                refresh_token=os.environ["SPOTIFY_USER_REFRESH"],
            )
            client = tekore.Spotify(token.access_token)
        except Exception as error:
            print_error("FAILED to initialize Spotify.")
            return [error]

        errors = list[Exception]()
        for playlist_config in self.config["spotify"]:
            updater = SpotifyPlaylistUpdater(playlist_config, client)
            playlist_id = playlist_config["playlist_id"]
            comment = playlist_config["comment"] or "?"
            try:
                updater.update(self.today)
            except Exception as error:
                print_error(
                    f"FAILED to update Spotify playlist {playlist_id} "
                    f"({comment})."
                )
                errors.append(error)
            else:
                print(f"Updated Spotify playlist {playlist_id} ({comment}).")

        return errors


def main() -> None:
    dotenv.load_dotenv()

    args = parser.parse_args()
    date_to_update_to: date = args.date_to_update_to
    config_path: Path = args.config_path
    schema_path = Path(__file__).parent / "bios.schema.json"

    bios_config = load_bios_config(config_path, schema_path)
    program = CountersProgram(bios_config, date_to_update_to)
    errors = program.run_all()
    dump_and_exit(errors)


if __name__ == "__main__":
    main()
