#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instagram_profile.py
23 June 2022 22:19:21

Simple script using web-scraping to update my Instagram
account profile with the HSSEAS day count.
"""

import json
import os
import sys
from datetime import date

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

# from selenium.webdriver.remote.webelement import WebElement
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.wait import WebDriverWait

"""
# waiting boilerplate:
element = WebDriverWait(driver, 10).until(
	EC.presence_of_element_located((By.LINK_TEXT, "Beginner Python Tutorials"))
)
"""

DRIVER_PATH = "C:/Users/soula/AppData/Local/Programs/Python/Python310/Scripts/MicrosoftWebDriver.exe"

# this is a thing you can do apparently
# and then: options.add_argument(f"user-data-dir={USER_DATA_PATH}")
# USER_DATA_PATH = "C:/Users/soula/AppData/Local/Microsoft/Edge/User Data/"

WAIT_TIMEOUT = 5.0  # seconds
INSTAGRAM_URL = "https://www.instagram.com/direct/inbox/"
START_DATE = date(2022, 6, 11)
BIOS_PATH = "../bios.json"

with open(BIOS_PATH, "rt") as file:
    bios: dict[str, str] = json.load(file)

BIO_TEMPLATE = bios["instagram"]


def login(driver: webdriver.Edge) -> None:
    load_dotenv()

    # find elements
    username_elem = driver.find_element("xpath",
                                        "//*[@id=\"loginForm\"]/div/div[1]/div/label/input")
    password_elem = driver.find_element("xpath",
                                        "//*[@id=\"loginForm\"]/div/div[2]/div/label/input")
    login_button = driver.find_element("xpath",
                                       "//*[@id=\"loginForm\"]/div/div[3]/button/div")

    username_elem.clear()
    username_elem.send_keys(os.environ["INSTAGRAM_USERNAME"])
    password_elem.clear()
    password_elem.send_keys(os.environ["INSTAGRAM_PASSWORD"])
    print("succesfully inputted credentials")

    login_button.click()
    print("logging in...")


def navigate_to_profile(driver: webdriver.Edge) -> None:
    try:
        avatar_elem = driver.find_element("xpath",
                                          "//*[@id=\"react-root\"]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[1]/span/img")
        avatar_elem.click()

        # full xpath needed since xpath had a variable part
        profile_elem = driver.find_element("xpath",
                                           "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/a[1]/div/div[2]/div/div/div/div")
        profile_elem.click()
    # idfk why this happens
    except WebDriverException as e:
        print(f"{type(e).__name__}: {e}")

    # edit button class:
    # "oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl _acan _acap _acat _acaw _a6hd"
    # edit button full xpath:
    # "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div[1]/div[1]/section/main/div/header/section/div[2]/div/a"

    # fuck it, directly using the href lmao
    driver.get("https://www.instagram.com/accounts/edit/")


# copy-pasted from coding_mix/coding_mix.pyw
def day_number() -> int:
    """Return day number since start, with START_DATE as Day 1."""
    return (date.today() - START_DATE).days + 1  # +1 to start at Day 1


def update_profile(driver: webdriver.Edge) -> None:
    new_bio = BIO_TEMPLATE.format(day_num=day_number())

    bio_box = driver.find_element("xpath",
                                  "//*[@id=\"pepBio\"]")
    bio_box.clear()
    bio_box.send_keys(new_bio)
    print(f"typed {new_bio=}")

    submit_button = driver.find_element("xpath",
                                        "/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/article/form/div[10]/div/div/button")
    submit_button.click()
    print("submitted profile change")


def main() -> None:
    """Main driver function."""

    service = Service(DRIVER_PATH)
    options = Options()

    # run without browser popup
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--headless"):
        options.add_argument("headless")

    # remember to update Edge browser itself to match driver version
    # msedgedriver.exe needs to be in PATH but it keeps not detecting
    driver: webdriver.Edge = webdriver.Edge(service=service, options=options)
    driver.get(INSTAGRAM_URL)

    # wait for page to load
    driver.implicitly_wait(WAIT_TIMEOUT)

    login(driver)
    navigate_to_profile(driver)
    update_profile(driver)

    print("successfully executed process")
    driver.quit()
    print("successfully terminated script")


if __name__ == "__main__":
    main()
