import json
from datetime import datetime

import jsonschema

from .config import DATE_FORMAT, JSON_FILE_PATH, JSON_SCHEMA_PATH


def load_bio_config_json() -> dict:  # TODO: Define a better type for this.
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
