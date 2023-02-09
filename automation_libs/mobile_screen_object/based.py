#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""

from abc import ABC
from os import environ

from .setup_driver import MOBILE_DRIVER


class BasedPage(ABC):
    def __init__(self):
        self.driver = MOBILE_DRIVER
        self.version = environ.get('VERSION')

    def announce_version(self):
        self.driver.logger.info('', timestamp=None)
        self.driver.logger.info(f'The test is conducted '
                                f'under version {self.version}')

    def _click_on_locator(self, locator: str, timeout: int = -1):
        self.driver.click_on_locator_with_wait_explicit(
            locator=locator, timeout=timeout
        )

    def _send_string_to_locator(self, locator: str, str_to_be_sent: str):
        self.driver.send_string_with_wait_explicit(
            locator=locator,
            str_to_be_sent=str_to_be_sent)
