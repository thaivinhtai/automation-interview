#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

"""


from getpass import getuser
from json import loads, dumps

from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choice, randint, uniform
from allure import attach
from allure_commons.types import AttachmentType
import allure

from robot.libraries.BuiltIn import BuiltIn

from framework_modules import CustomLogger, INTERNAL_PATH


CURRENT_TEST_NAME = BuiltIn().get_variable_value("${TEST_MODULE}")
LOGGER = CustomLogger(CURRENT_TEST_NAME)


ALLURE_ATTACHMENT_TYPE = {
    'txt': AttachmentType.TEXT,
    'csv': AttachmentType.CSV,
    'tsv': AttachmentType.TSV,
    'uri': AttachmentType.URI_LIST,
    "html": AttachmentType.HTML,
    "xml": AttachmentType.XML,
    "json": AttachmentType.JSON,
    "yaml": AttachmentType.YAML,
    "yml": AttachmentType.YAML,
    "pcap": AttachmentType.PCAP,
    "png": AttachmentType.PNG,
    "jpg": AttachmentType.JPG,
    "svg": AttachmentType.SVG,
    "gif": AttachmentType.GIF,
    "bmp": AttachmentType.BMP,
    "tiff": AttachmentType.TIFF,
    "mp4": AttachmentType.MP4,
    "ogg": AttachmentType.OGG,
    "webm": AttachmentType.WEBM,
    "pdf": AttachmentType.PDF,
}


def log_current_executor() -> None:
    """Log current executor's info.

    This function helps to log current tester, who executes the test case.

    Returns
    -------
    None
    """
    current_user = getuser()
    current_dir = INTERNAL_PATH.workspace_path
    LOGGER.info("", timestamp=False)
    LOGGER.info(f'Test case ' +
                f'is conducted by: {current_user}')
    LOGGER.info(f'Workspace locates at {current_dir}')
    LOGGER.info(f'========== Test Case Begins ==========')


def attach_file_to_report(attachments: list) -> None:
    """Attach logfile in text to Allure report.

    Returns
    -------
    None
    """
    for attachment in attachments:
        try:
            attachment_file = open(attachment, 'rb')
            file_type = attachment.split("/")[-1].split('.')[-1]
            attach_file = attachment_file.read()
            attach(attach_file, name='attachment',
                   attachment_type=ALLURE_ATTACHMENT_TYPE.get(file_type))
            attachment_file.close()
        except FileNotFoundError as ex:
            print('Could not attach log file.', ex)
