#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains function that generates log folders.
"""

from datetime import datetime
from os import mkdir, path
from .internal_path import INTERNAL_PATH
from .args_parser import ARGUMENTS


def generate_current_time_execution_log_dir() -> None:
    """Create and return path of folder that stores current time log files.

    This function takes the timestamp when test cases are run, then create
    directories to store log files. The directory is under module and its name
    is the current time (hh-mmm-ss).

    The structure of generated folders:
        workspace/{today}/{module}/{current_time}

    Returns
    -------
    None
    """
    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H-%M-%S")

    today_log_folder = f'{INTERNAL_PATH.log_dir_path}/{today}'
    module_in_lower = [element.lower() for element in ARGUMENTS.module]
    if 'all' in module_in_lower:
        module_in_lower = INTERNAL_PATH.test_modules

    module_log_folders = {
        module_name:  f'{today_log_folder}/{module_name}' for module_name
        in module_in_lower if module_name in INTERNAL_PATH.test_modules
    }

    current_time_execution_log_dir = {
        module_name: f'{module_log_folder}/{current_time}'
        for module_name, module_log_folder in module_log_folders.items()
    }

    for directory in (INTERNAL_PATH.log_dir_path, today_log_folder,
                      *module_log_folders.values(),
                      *current_time_execution_log_dir.values()):
        if not path.exists(directory):
            mkdir(directory)

    # update path to InternalPath instance attribute.
    INTERNAL_PATH.current_execution_log_dir.update(
        current_time_execution_log_dir
    )
