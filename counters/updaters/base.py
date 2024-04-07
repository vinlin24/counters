from abc import ABC, abstractmethod
from datetime import date
from typing import Generic, TypeVar

import rich.panel
from selenium import webdriver

DetailsDict = TypeVar("DetailsDict")


class Updater(ABC, Generic[DetailsDict]):
    """
    Generic ABC to inherit from to implement updating the bio on some
    social media platform.
    """

    def __init__(self, data: dict) -> None:
        """Initialize the updater.

        Args:
            data (dict): Loaded configuration JSON for this updater.
        """
        self.data = data

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """The name of the platform this updater is for."""

    @abstractmethod
    def prepare_details(self, today: date) -> DetailsDict:
        """Prepare the details to use when updating the bio."""

    @abstractmethod
    def update_bio(self, details: DetailsDict, driver: webdriver.Edge) -> None:
        """Update the bio (or equivalent) on social media platform."""

    @abstractmethod
    def format_preview(self, details: DetailsDict) -> rich.panel.Panel:
        """Format the console presentation of this task."""
