# Status Day Counters

> :mega: This README is mostly for future me if I decide to come back and review/enhance this project. If by any chance you are a stray visitor, you're welcome to use this code and instructions to mess around with your social media accounts too.

## Description

Sometimes I want my status to keep track of certain day counts, like "Day X of..." For example, my GitHub bio is currently set up to say "Day X of waiting for HSSEAS to let me let them let me in", in passive protest to how I'm still not allowed to apply for my switch to Computer Science. [Check it out](https://github.com/vinlin24) right now!

I originally had a few standalone, hard-coded scripts for Discord, Instagram, and Spotify. This project seeks to just bring them together and one place and make them more configurable. The original standalone scripts are included in the [standalones/](standalones/) directory just for record. I am 100% sure they do not work anymore.

## Configuration

I placed a configuration file at:
```powershell
"$env:USERPROFILE\.config\counters\bios.json"
```
If it's missing, you should make one at this path. A log file is also maintained in this directory.

As of now, the `bios.json` file should have the following schema:

```json
{
  "discord": {
    "status": "string | null",
    "start": "YYYY-MM-DD | null"
  },
  "instagram": {
    "bio": "string | null",
    "start": "YYYY-MM-DD | null"
  },
  "spotify": [
    {
      "comment": "any",
      "playlist_id": "string",
      "name": "string | null",
      "description": "string | null",
      "start": "YYYY-MM-DD | null"
    },
    {
      "comment": "any",
      "playlist_id": "string",
      "name": "string | null",
      "description": "string | null",
      "start": "YYYY-MM-DD | null"
    }
  ],
  "github": {
    "bio": "string | null",
    "start": "YYYY-MM-DD | null"
  }
}
```

- The strings to display (`status`, `bio`, `description`) can include, but don't need to, a `{0}` placeholder for where the day number will go. Example:
  ```json
  {
    "description": "day {0} of waiting for kaguya season 4"
  }
  ```
- The `start` keys are dates to be considered as "Day 1" in the count.
- For each Spotify playlist entry, you have the option to change either the playlist name, description, or both. Leaving a key as `null` signifies leaving it unchanged.
- The `comment` keys are not used. They're just a way to document each playlist entry for yourself.

## Usage

Since this program is meant to automate, it should be hooked up to a [scheduler](#setup) to be run periodically. That way, the statuses on all platforms update automatically, and all you need to do when you want to change the templates is edit the [bios.json file](#configuration).

But for debugging/development purposes, the code can be run on demand with some command line options:

```powershell
cd path\to\this\repo
.venv\Scripts\Activate.ps1
python -m counters <# options #>
```

| Option           | Description                                                                                                                                                             |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-c/--console`   | Only output to the console. Do not write to the log file and do not send an email upon failure.                                                                         |
| `-w/--window`    | Run the Selenium web scraper in an open browser window instead of headlessly.                                                                                           |
| `-d/--discord`   | See below.                                                                                                                                                              |
| `-i/--instagram` | See below.                                                                                                                                                              |
| `-s/--spotify`   | If any of these 3 switches are included, run these select tasks. Otherwise if all 3 switches are absent from the command line, use the default behavior of running all. |

## Setup

I use Windows Task Scheduler, and below is my current setup:

### General

When running the task, use the following user account: (my `$env:USERNAME`)

- [x] Run whether user is logged on or not

### Triggers

| Trigger   | Details               | Status  |
| --------- | --------------------- | ------- |
| Daily     | At 12:00 AM every day | Enabled |
| At log on | At log on of any user | Enabled |

### Actions

| Action          | Program/script                              | Arguments   | Start in          |
| --------------- | ------------------------------------------- | ----------- | ----------------- |
| Start a program | path\to\this\repo\\.venv\Scripts\python.exe | -m counters | path\to\this\repo |

### Conditions

- [x] Start only if the following network connection is available: Any connection

### Settings

- [x] Allow task to be run on demand
- [x] Stop the task if it runs longer than: 1 hour
- [x] If the running task does not end when requested, force it to stop

If tha task is already running, then the following rule applies: Do not start a new instance

## Environment Recovery

This project makes use of an `.env` file to store sensitive values as environment variables. The required keys are:

- `DISCORD_EMAIL`
- `DISCORD_PASSWORD`
- `INSTAGRAM_USERNAME`
- `INSTAGRAM_PASSWORD`
- `SPOTIFY_CLIENT_ID`
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_USER_REFRESH`
- `GITHUB_PROFILE_URL`
- `GITHUB_EMAIL`
- `GITHUB_PASSWORD `
- `ERROR_EMAIL`
- `ERROR_EMAIL_PASSWORD`

You should obviously know your own email, username, and password credentials. `GITHUB_PROFILE_URL` happens to be https://github.com/vinlin24 for me. `ERROR_EMAIL` and `ERROR_EMAIL_PASSWORD` is the email and password to send and receive error reports.

`SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` can be found/regenerated for your application on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications). The user refresh token, `SPOTIFY_USER_REFRESH`, can be regenerated by running a throwaway script:

```python
# pip install tekore
import tekore

CLIENT_ID = "SPOTIFY CLIENT ID"
CLIENT_SECRET = "SPOTIFY CLIENT SECRET"
token = tekore.request_client_token(CLIENT_ID, CLIENT_SECRET)

# This is your refresh token, save it somewhere
print(token.refresh_token)
```

The state of the project virtual environment is maintained in [requirements.txt](requirements.txt). You can recreate the environment like you normally would:
```
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

See [Usage](#usage) for how to run the package.

## Implementation Details

The Spotify part uses the [tekore](https://tekore.readthedocs.io/en/stable/index.html) library as a wrapper for the [Spotify Web API](https://developer.spotify.com/documentation/web-api/). This is a robust and actively maintained library, so I do not worry much about having to modify this part of the code.

The Discord and Instagram parts use [Selenium](https://selenium-python.readthedocs.io/) webscraping to navigate the respective web applications and update my user status/bio since they lack APIs that support such an action. The problem with this is that their implementations risk breaking every update because they rely on XPaths and CSS selectors of web elements that can change unexpectedly. For example, the XPaths found in my original [discord_profile.py](counters/update_discord.py) are no longer applicable.

The package looks for the Edge web driver executable within the package itself by the name of `msedgedriver.exe`. Download the version compatible with the current version of your Edge web browser from [the official website](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) and place it in the root of the package (same level as [`__init__.py`](counters/__init__.py)). The code has been changed such that a new path does not have to be written into the source code upon each update; instead, it trusts the invariant that `mesedgedriver.exe` is found in the package.

Updated: If an error in any part of the main process is raised, it is compiled in an email sent to myself in addition to logging it to the log file.

Don't forget to update the [JSON schema](#configuration) part of this documentation if you choose to add new features that affect it.
