#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module handles custom testing library generating.
"""

from datetime import datetime
from os import mkdir, path

from robot.testdoc import testdoc

from .internal_path import INTERNAL_PATH


def generate_docs() -> None:
    """Generate documentation of test cases.

    This function generates folder that stores documentations before generate
    document files.

    The folder structure are classified by:
        {workspace}/documentations/{date}/{module}/{current_time}/{test_suite}

    Returns
    -------
    None
    """
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H-%M-%S")
    doc_path = INTERNAL_PATH.document_dir

    today_doc_folder = f'{doc_path}/{today}'
    module_doc_folder = [f'{today_doc_folder}/{test_module}'
                         for test_module in INTERNAL_PATH.test_modules]

    for folder in (doc_path, today_doc_folder, *module_doc_folder):
        if not path.exists(folder):
            mkdir(folder)

    for folder in module_doc_folder:
        if not path.exists(f"{folder}/{current_time}"):
            mkdir(f"{folder}/{current_time}")

    for test_module in INTERNAL_PATH.test_modules:
        for suite_name, suite_file \
                in INTERNAL_PATH.test_suites_of_module(test_module).items():
            doc_out_file = f'{today_doc_folder}/{test_module}/{current_time}' \
                           f'/{suite_name}_document.html'
            testdoc(suite_file, doc_out_file,
                    title=suite_name)
