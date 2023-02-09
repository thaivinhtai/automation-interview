#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains functions and abstract class for the keywords lib in every
testing module.
"""


from abc import ABC
from datetime import datetime

from json import loads

from robot.libraries.BuiltIn import BuiltIn
from robot.utils import get_link_path
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, InvalidElementStateException, \
    StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

from framework_modules import CustomLogger, INTERNAL_PATH

from framework_modules.fundamental_auto_libs import attach_file_to_report


class AbstractDriver(ABC):
    """
    This abstract class is a blueprint for common keyword for each testing
    module.
    """

    def __init__(self, context_by: object):
        """Constructor."""
        self.test_module = BuiltIn().get_variable_value("${TEST_MODULE}")
        self.logger = CustomLogger(self.test_module)
        self.driver = None
        self.implicitly_wait = 5
        self.default_explicit_wait = 5
        self.context_by = context_by
        self.current_test_name = BuiltIn().get_variable_value("${TEST NAME}")
        self.element_mapping = {
            'xpath': self.context_by.XPATH,
            'id': self.context_by.ID,
            'name': self.context_by.NAME,
            'partial_text': self.context_by.PARTIAL_LINK_TEXT,
            'css_selector': self.context_by.CSS_SELECTOR,
            'class_name': self.context_by.CLASS_NAME,
            'tag_name': self.context_by.TAG_NAME
        }

    @staticmethod
    def __split_element_value(locator: str) -> tuple:
        """Split element value.

        Parameters
        ----------
        locator : str

        Returns
        -------
        tuple
            locator and its type
        """
        value = locator.split("=", 1)
        location_type = value[0]
        location = value[1]
        return location, location_type

    def get_element(self, locator: str):
        """Get element.

        This function resolves the webview element identifier.

        Parameters
        ----------
        locator : str

        Returns
        -------
        The Webview Element.
        """
        locator, locator_type = self.__split_element_value(locator)
        if locator_type == "coordinate":
            return loads(locator)
        try:
            return self.driver.find_element(
                self.element_mapping.get(locator_type), locator)
        except NoSuchElementException:
            self.take_screenshot()
            raise NoSuchElementException

    def get_elements(self, locator: str):
        """Get element.

        This function resolves the webview element identifier.

        Parameters
        ----------
        locator : str

        Returns
        -------
        The Webview Element.
        """
        locator, locator_type = self.__split_element_value(locator)
        try:
            return self.driver.find_elements(
                self.element_mapping.get(locator_type), locator)
        except NoSuchElementException:
            self.take_screenshot()
            raise NoSuchElementException

    def wait_explicit(self, condition: str, locator: str,
                      timeout: int = -1, inverse: bool = False) -> bool:
        """

        Parameters
        ----------
        condition
        locator
        timeout
        inverse

        Returns
        -------
        bool
        """
        if timeout < 0:
            timeout = self.default_explicit_wait
        mapping_condition = {
            'presence_of_element_located': ec.presence_of_element_located,
            'visibility_of_element_located': ec.visibility_of_element_located,
            'presence_of_all_elements_located':
                ec.presence_of_all_elements_located,
            'invisibility_of_element_located':
                ec.invisibility_of_element_located,
            'element_to_be_clickable': ec.element_to_be_clickable,
            'element_located_to_be_selected':
                ec.element_located_to_be_selected,
        }
        locator, locator_type = self.__split_element_value(locator)
        wait = WebDriverWait(self.driver, timeout)
        condition = mapping_condition.get(condition)
        try:
            if not inverse:
                wait.until(condition((self.element_mapping.get(locator_type),
                                     locator)))
                return True
            wait.until_not(condition((self.element_mapping.get(locator_type),
                                     locator)))
            return True
        except TimeoutException:
            return False

    def take_screenshot(self) -> None:
        """Take screenshot.

        Take screenshot then attach to robot log and appium result.

        Returns
        -------
        None
        """
        current_time = datetime.now().strftime("%H-%M-%S")
        screenshot_name = f"{self.current_test_name}_{current_time}.png"
        screenshot_path = \
            f"{INTERNAL_PATH.current_screenshot_dir.get(self.test_module)}/" \
            f"{screenshot_name}"
        while "'" in screenshot_path:
            screenshot_path = screenshot_path.replace("'", "")
        while '"' in screenshot_path:
            screenshot_path = screenshot_path.replace('"', '')
        self.driver.save_screenshot(screenshot_path)
        self.logger.debug(f'Take screenshot {screenshot_path}')
        attach_file_to_report([screenshot_path])
        link_path = get_link_path(
            screenshot_path,
            INTERNAL_PATH.current_robot_report_dir.get(self.test_module))
        self.logger.info(
            f'<a href="{link_path}"><img src="{link_path}" '
            f'width="1500"></a>',
            html=True)

    def click_on_element(self, locator: str) -> None:
        if locator.split("=")[0] == "coordinate":
            return self.click_on_coordinate(self.get_element(locator))
        try:
            self.get_element(locator).click()
        except (StaleElementReferenceException,
                ElementNotInteractableException):
            self.take_screenshot()
        self.logger.debug(f'click to {locator}')

    def send_string_to_element(self, locator: str,
                               str_to_be_sent: str) -> None:
        try:
            self.get_element(locator).clear()
        except IndexError:
            self.logger.warn("Can not clear before send new string on mobile")
        except InvalidElementStateException:
            self.get_element(locator).send_keys(Keys.DELETE)
        self.logger.debug(f'Send "{str_to_be_sent} to {locator}')
        self.get_element(locator).send_keys(str_to_be_sent)

    def click_on_coordinate(self, coordinate) -> None:
        """

        Parameters
        ----------
        coordinate

        Returns
        -------

        """
        pass

    def click_on_locator_with_wait_explicit(self, locator: str,
                                            timeout: int = -1):
        """

        """
        result = self.wait_explicit(condition="element_to_be_clickable",
                                    locator=locator, timeout=timeout)
        if not result:
            self.logger.error(
                f"The locator {locator} is not clickable.")
            self.take_screenshot()
        self.click_on_element(locator)

    def send_string_with_wait_explicit(self, locator: str,
                                       str_to_be_sent: str,
                                       timeout: int = -1):
        """

        """
        result = self.wait_explicit(
            condition="presence_of_element_located",
            locator=locator, timeout=timeout)
        if not result:
            self.logger.error(
                f"The locator {locator} is not present.")
            self.take_screenshot()
        self.send_string_to_element(locator=locator,
                                    str_to_be_sent=str_to_be_sent)
