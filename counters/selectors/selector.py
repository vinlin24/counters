from enum import Enum
from typing import Iterator

from selenium.webdriver.common.by import By


# Convert to enum for type hinting... is there a better way to do this?
class ByStrategy(Enum):
    ID = By.ID
    XPATH = By.XPATH
    LINK_TEXT = By.LINK_TEXT
    PARTIAL_LINK_TEXT = By.PARTIAL_LINK_TEXT
    NAME = By.NAME
    TAG_NAME = By.TAG_NAME
    CLASS_NAME = By.CLASS_NAME
    CSS_SELECTOR = By.CSS_SELECTOR


class Selector:
    """
    Convenience dataclass for grouping a value with its corresponding
    Selenium `By` strategy. Supports unpacking::

        # Before:
        driver.find_element(By.CSS_SELECTOR, SOME_CONSTANT)
        # After:
        driver.find_element(...selector)
    """

    def __init__(self, by: ByStrategy, value: str) -> None:
        self.by = by.value
        self.value = value

    def __iter__(self) -> Iterator[str]:
        return iter((self.by, self.value))


class CSSSelector(Selector):
    def __init__(self, selector: str) -> None:
        super().__init__(ByStrategy.CSS_SELECTOR, selector)


class XPathSelector(Selector):
    def __init__(self, xpath: str) -> None:
        super().__init__(ByStrategy.XPATH, xpath)
