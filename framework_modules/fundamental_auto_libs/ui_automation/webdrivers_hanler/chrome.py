#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chrome.
"""

from os import listdir

from selenium import webdriver

from chromedriver_autoinstaller import get_chrome_version
from undetected_chromedriver import Chrome, ChromeOptions
from chromedriver_autoinstaller.utils import (
    get_matched_chromedriver_version, check_version, get_platform_architecture,
    get_chromedriver_url, get_chromedriver_filename
)

from ._chromium import download_chromium_driver, get_chromium_driver

from framework_modules import INTERNAL_PATH


def get_chromedriver():
    """Get chromedriver.

    Check if there is a chromedriver corresponding to the current chrome
    version. If not, auto download the corresponding one.

    Returns
    -------
    str
        Absolute path to the chromedriver.
    """
    # Get chrome version on local machine
    current_client_chrome_version = get_chrome_version()
    # Get chromedriver that is needed for automation
    chromedriver_version = \
        get_matched_chromedriver_version(current_client_chrome_version)

    # Check if there is an existed chromedriver could be used
    for file_ in listdir(INTERNAL_PATH.chromedriver_dir):
        if check_version(f'{INTERNAL_PATH.chromedriver_dir}/{file_}',
                         chromedriver_version):
            chrome_binary_path = f'{INTERNAL_PATH.chromedriver_dir}/{file_}'
            return chrome_binary_path

    # Get chromedriver download url
    chromedriver_download_url = get_chromedriver_url(chromedriver_version)
    # Check platform and architect of machine's OS
    platform, architect = get_platform_architecture()

    return download_chromium_driver(
        platform=platform, architect=architect, chromium_distro="chrome",
        chromium_version=chromedriver_version,
        chromium_download_url=chromedriver_download_url,
        chromium_driver_folder=INTERNAL_PATH.chromedriver_dir,
        get_chromium_driver_file_name=get_chromedriver_filename
    )


def get_undetected_chrome() -> webdriver:
    """This function establishes chrome browser."""
    return get_chromium_driver(
        chromium_options=ChromeOptions(),
        chromium_driver=Chrome, headless=False, driver=get_chromedriver()
    )
