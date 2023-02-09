#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chrome.
"""

from urllib.request import urlopen
from urllib.error import URLError

from os import access, X_OK, chmod

from io import BytesIO
from shutil import move
from zipfile import ZipFile

from selenium import webdriver


def download_chromium_driver(**kwargs) -> str:
    """

    """
    chromium_distro = kwargs.get('chromium_distro', "chrome")
    platform = kwargs.get('platform')
    architect = kwargs.get('architect')
    chromium_version = kwargs.get('chromium_version')
    current_client_chromium_version = kwargs.get(
        'current_client_chromium_version')
    chromium_download_url = kwargs.get('chromium_download_url')
    chromium_download_url_backup = kwargs.get('chromium_download_url_backup')
    chromium_driver_folder = kwargs.get("chromium_driver_folder")
    get_chromium_driver_file_name = kwargs.get("get_chromium_driver_file_name")

    # Chromium Driver filename
    extension = ''
    if platform == 'win':
        extension = '.exe'
    chromium_driver_binary_path = \
        f'{chromium_driver_folder}' \
        f'/{chromium_distro}driver_{platform}{architect}_v{chromium_version}' \
        f'{extension}'

    # Download chromedriver
    try:
        response = urlopen(chromium_download_url)
        if response.getcode() != 200:
            raise URLError('Not Found')
    except URLError:
        try:
            response = urlopen(chromium_download_url_backup)
            chromium_driver_binary_path = chromium_driver_binary_path.replace(
                chromium_version, current_client_chromium_version
            )
        except URLError:
            raise RuntimeError(f'Failed to download chromedriver archive: '
                               f'{chromium_download_url} or'
                               f'{chromium_download_url_backup}')
    archive = BytesIO(response.read())
    with ZipFile(archive) as zip_file:
        chromium_driver_filename = get_chromium_driver_file_name()
        zip_file.extract(chromium_driver_filename, chromium_driver_folder)
        move(
            f'{chromium_driver_folder}/{chromium_driver_filename}',
            chromium_driver_binary_path
        )

    # Check access mode of the current chromedriver
    if not access(chromium_driver_binary_path, X_OK):
        chmod(chromium_driver_binary_path, 0o744)

    return chromium_driver_binary_path


def get_chromium_driver(**kwargs) -> webdriver:
    """

    """
    chromium_options = kwargs.get("chromium_options")
    chromium_driver = kwargs.get("chromium_driver")
    headless = kwargs.get("headless")
    driver = kwargs.get("driver")
    browser_executable_path = kwargs.get("browser_executable_path")

    if headless:
        chromium_options.add_argument('--headless')
        chromium_options.add_argument('--disable-extensions')
        chromium_options.add_argument('--disable-gpu')  # For windows os only
        # bypass OS security model
        chromium_options.add_argument('--no-sandbox')
        # overcome limited resource problems
        chromium_options.add_argument('--disable-dev-shm-usage')
    chromium_options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })
    try:
        return chromium_driver(
            options=chromium_options, executable_path=driver,
            driver_executable_path=driver,
            browser_executable_path=browser_executable_path
        )
    except TypeError:
        return chromium_driver(options=chromium_options,
                               executable_path=driver)
