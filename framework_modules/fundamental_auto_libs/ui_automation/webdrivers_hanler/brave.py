#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chrome.
"""

from os import listdir

from selenium import webdriver

from subprocess import Popen, PIPE

from chromedriver_autoinstaller.utils import (
    get_matched_chromedriver_version, check_version, get_platform_architecture,
    get_chromedriver_url, get_chromedriver_filename
)
from undetected_chromedriver import Chrome, ChromeOptions

from ._chromium import download_chromium_driver, get_chromium_driver

from framework_modules import INTERNAL_PATH


def get_brave_driver():
    """Get brave driver.

    Check if there is a chromedriver corresponding to the current brave
    version. If not, auto download the corresponding one.

    Returns
    -------
    str
        Absolute path to the chromedriver.
    """
    # Check platform and architect of machine's OS
    platform, architect = get_platform_architecture()

    # Get Brave version on local machine
    if platform != "mac":
        # TODO: procedure to support other OS.
        current_client_brave_version = ""
        pass
    else:
        process = Popen(
            ['/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
             '--version'], stdout=PIPE)
        current_client_brave_version = process.communicate()[0]\
            .decode('UTF-8').replace('Brave Browser', '').strip()
    # Get chromedriver that is needed for automation
    chromedriver_version = \
        get_matched_chromedriver_version(current_client_brave_version)

    # Check if there is an existed chromedriver could be used
    for file_ in listdir(INTERNAL_PATH.chromedriver_dir):
        if check_version(f'{INTERNAL_PATH.chromedriver_dir}/{file_}',
                         INTERNAL_PATH.chromedriver_dir):
            return f'{INTERNAL_PATH.chromedriver_dir}/{file_}'

    # Get chromedriver download url
    chromedriver_download_url = get_chromedriver_url(chromedriver_version)

    return download_chromium_driver(
        platform=platform, architect=architect,
        chromium_version=chromedriver_version,
        chromium_download_url=chromedriver_download_url,
        chromium_driver_folder=INTERNAL_PATH.chromedriver_dir,
        get_chromium_driver_file_name=get_chromedriver_filename
    )


def get_undetected_brave() -> webdriver:
    """This function establishes chrome browser."""
    brave_options = ChromeOptions()
    brave_binary = None
    if get_platform_architecture()[0] == 'mac':
        brave_binary = \
            '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
        brave_options.binary_location = brave_binary
    return get_chromium_driver(
        chromium_options=brave_options, chromium_driver=Chrome,
        headless=False, driver=get_brave_driver(),
        browser_executable_path=brave_binary
    )
