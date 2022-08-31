#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
discord_profile.py
10 July 2022 13:03:05

Selenium script for updating Discord custom status.
"""

import argparse
import json
import os
import sys
from datetime import date

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.remote.webelement import WebElement

DRIVER_PATH = "C:/Users/soula/AppData/Local/Programs/Python/Python310/Scripts/MicrosoftWebDriver.exe"

WAIT_TIMEOUT = 5.0  # seconds
DISCORD_URL = "https://discord.com/login"
START_DATE = date(2022, 6, 11)
BIOS_PATH = "../bios.json"

with open(BIOS_PATH, "rt") as file:
    bios: dict[str, str] = json.load(file)

HSSEAS_TEMPLATE = "day {day_num} of waiting for HSSEAS to let me in"

# full xpaths

XPATH_LOGIN_BUTTON = "/html/body/div[1]/div/div/div[1]/div[1]/header[1]/nav/div/a"
XPATH_EMAIL_INPUT = "/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[1]/div[2]/div[1]/div/div[2]/input"
XPATH_PASSWORD_INPUT = "/html/body/div[1]/div[2]/div/div[1]/div/div/div/div/form/div/div/div[1]/div[2]/div[2]/div/input"
XPATH_AVATAR_ICON = "/html/body/div[1]/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div[2]/div[1]/section/div[2]/div[1]/div"
XPATH_CUSTOM_STATUS = "/html/body/div[1]/div[2]/div/div[3]/div/div/div/div/div[7]/div"
XPATH_STATUS_INPUT = "/html/body/div[1]/div[2]/div/div[3]/div[2]/div/div/div[2]/div[1]/div[2]/div/div[2]/input"


class Parser(argparse.ArgumentParser):
    def __init__(self) -> None:
        super().__init__(description="Update discord status through Selenium")
        self.add_argument("--headless", "-l", action="store_true",
                          help="run the driver headlessly (no window popup)")
        self.add_argument("--use-bios", "-u", action="store_true",
                          help="use the status in bios.json")
        self.add_argument("status", nargs="*", default=None,
                          help="custom status if not using HSSEAS counter")


def setup(headless: bool) -> webdriver.Edge:
    service = Service(DRIVER_PATH)
    options = Options()

    # run without browser popup
    # this sends a lot of weird stuff to console output but works
    if headless:
        options.headless = True

    # remember to update Edge browser itself to match driver version
    # msedgedriver.exe needs to be in PATH but it keeps not detecting
    return webdriver.Edge(service=service, options=options)


def login(driver: webdriver.Edge) -> None:
    load_dotenv()

    # enter credentials
    email_input = driver.find_element("xpath",
                                      XPATH_EMAIL_INPUT)
    password_input = driver.find_element("xpath",
                                         XPATH_PASSWORD_INPUT)
    email_input.clear()
    email_input.send_keys(os.environ["DISCORD_EMAIL"])
    password_input.clear()
    password_input.send_keys(os.environ["DISCORD_PASSWORD"] + "\n")
    print("successfully inputted credentials")


def find_status_input(driver: webdriver.Edge) -> WebElement:
    avatar_icon = driver.find_element("xpath",
                                      XPATH_AVATAR_ICON)
    avatar_icon.click()

    custom_status = driver.find_element("xpath",
                                        XPATH_CUSTOM_STATUS)
    custom_status.click()

    status_input = driver.find_element("xpath",
                                       XPATH_STATUS_INPUT)
    return status_input


def update_status(status_input: WebElement, ns: argparse.Namespace) -> None:
    if ns.use_bios:
        with open(BIOS_PATH, "rt") as file:
            bios = json.load(file)
            status: str = bios["discord"]
    else:
        status = HSSEAS_TEMPLATE

    # attempt to format (HSSEAS counter)
    status = status.format(day_num=day_number())

    status_input.clear()
    status_input.send_keys(status + "\n")
    print(f"inputted {status=}")


# copy-pasted from coding_mix/coding_mix.pyw
def day_number() -> int:
    """Return day number since start, with START_DATE as Day 1."""
    return (date.today() - START_DATE).days + 1  # +1 to start at Day 1


def main() -> None:
    """Main driver function."""
    ns = Parser().parse_args(sys.argv[1:])

    driver = setup(ns.headless)

    driver.get(DISCORD_URL)
    # wait for page to load
    driver.implicitly_wait(WAIT_TIMEOUT)

    login(driver)
    status_input = find_status_input(driver)
    update_status(status_input, ns)

    print("successfully executed process")
    driver.quit()
    print("successfully terminated script")


if __name__ == "__main__":
    main()
