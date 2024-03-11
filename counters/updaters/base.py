from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, TypeVar

from selenium import webdriver

DetailsDict = TypeVar("DetailsDict")


class Updater(ABC, Generic[DetailsDict]):
    """
    Generic ABC to inherit from to implement updating the bio on some
    social media platform.
    """

    def __init__(self, data: dict, driver: webdriver.Edge) -> None:
        """Initialize the updater.

        Args:
            data (dict): Loaded configuration JSON.
            driver (webdriver.Edge): Selenium web driver instance. It is
            up to the implementation of the updater whether it makes use
            of it or not.
        """
        self.data = data
        self.driver = driver

    @abstractmethod
    def prepare_details(self, today: date) -> DetailsDict:
        """Prepare the details to use when updating the bio."""

    @abstractmethod
    def update_bio(self, details: DetailsDict) -> None:
        """Update the bio (or equivalent) on social media platform."""
