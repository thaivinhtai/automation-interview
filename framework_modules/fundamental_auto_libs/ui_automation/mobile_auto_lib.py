#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This module contain custom keyword for mobile testing."""

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.common.utils import is_url_connectable

from framework_modules import INTERNAL_PATH, ARGUMENTS, APPIUM_PROPERTIES
from test_data.common_variables import APP_DOWNLOAD_URL
from .ui_based_class import AbstractDriver


class MobileFundamentalAction(AbstractDriver):
    """

    """

    def __init__(self):
        """

        """

        super().__init__(MobileBy)

        self.device_name = ARGUMENTS.device_name
        self.default_timeout = '40000'
        self.platform = 'android'
        self.app = ARGUMENTS.app if ARGUMENTS.app else APP_DOWNLOAD_URL

        self.platform_version = ARGUMENTS.mobile_platform_ver

        self.port_to_listen = ARGUMENTS.appium_port

        self.element_mapping.update({
            'accessibility_id': self.context_by.ACCESSIBILITY_ID,
            'image': self.context_by.IMAGE
        })

        self.appium_remote_server = \
            f'http://127.0.0.1:{self.port_to_listen}/wd/hub'

        self.init_package = None
        self.init_activity = None

        self.window_size = None
        self.width = None
        self.height = None
        self.appium_server_session = None
        self.context = None
        self.contexts = None
        self.desired_cap = {}

    def set_driver(self):
        self.desired_cap.update({
            'platformName': self.platform,
            'platformVersion': self.platform_version,
            'deviceName': self.device_name,
            'app': self.app,
            'udid': APPIUM_PROPERTIES.mobile_udid,
            'fullReset': True,
            'enablePerformanceLogging': True,
            'ignoreUnimportantViews': True,
            'automationName': 'UIAutomator2',
            'adbExecTimeout': self.default_timeout,
            'newCommandTimeout': self.default_timeout,
            'autoGrantPermissions': True,
            'chromedriverExecutableDir': INTERNAL_PATH.chromedriver_dir,
            'chromedriverChromeMappingFile':
                INTERNAL_PATH.chromedriver_mapping_file,
            'chromedriverPort': APPIUM_PROPERTIES.chrome_driver_port,
            'mjpegServerPort': APPIUM_PROPERTIES.mjpeg_server_port
        })
        if ARGUMENTS.debug:
            self.desired_cap.pop('fullReset', None)

        self.driver = webdriver.Remote(self.appium_remote_server,
                                       self.desired_cap)
        self.init_activity = self.driver.current_activity
        self.init_package = self.driver.current_package
        self.window_size = self.driver.get_window_size()
        self.width = self.window_size.get("width")
        self.height = self.window_size.get("height")
        self.context = self.driver.context
        self.contexts = self.driver.contexts
        self.logger.info('', timestamp=False)
        self.logger.info(
            f'Execute test on {self.device_name}, platform {self.platform} '
            f'version {self.platform_version}'
        )

    def switch_context(self, context_name: str) -> None:
        """Switch context.

        Parameters
        ----------
        context_name : str

        Returns
        -------
        None
        """
        self.logger.debug(f'Current context: {self.driver.context}')
        self.logger.debug(f'Available contexts: {self.driver.contexts}')
        self.driver.switch_to.context(context_name)
        self.logger.debug(f'Switched to {context_name} context')

    def click_on_coordinate(self, coordinate) -> bool:
        """

        Parameters
        ----------
        coordinate

        Returns
        -------

        """
        action = TouchAction(self.driver)
        x = float(coordinate.get("x")) * self.width
        y = float(coordinate.get("y")) * self.height
        action.tap(x=x, y=y)
        self.logger.debug(f"Click on coordinate: (x={x}, y={y})")
        return True

    def swipe_horizontal(self, start: float = 0.9, end: float = 0.1) -> bool:
        """

        Parameters
        ----------
        start
        end

        Returns
        -------

        """
        self.driver.swipe(start_y=self.height*0.5, end_y=self.height*0.5,
                          start_x=self.width*start, end_x=self.width*end)
        return True

    def swipe_vertical(self, start: float = 0.9, end: float = 0.1) -> bool:
        """

        Parameters
        ----------
        start
        end

        Returns
        -------

        """
        self.driver.swipe(start_y=self.height*start, end_y=self.height*end,
                          start_x=self.width*0.5, end_x=self.width*0.5)
        return True

    def go_to_url(self, url: str):
        if not self.driver:
            self.set_driver()
        self.driver.get(url)
        self.logger.info('', timestamp=False)
        self.logger.info(f'Access {url}')

    def end_session(self):
        self.logger.info('End session.')
        self.driver.quit()
        self.driver = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.terminate_app()
        self.logger.debug('Close app')
        self.driver.quit()
        self.logger.debug('End session')


if __name__ == "__main__":
    print(type(is_url_connectable(4723)))
