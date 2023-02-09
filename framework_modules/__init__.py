#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The framework_modules package contains all modules
for running test cases and reporting.
"""


from .args_parser import ARGUMENTS
from .env_vars_setup import set_python_path_env_var
from .document_generator import generate_docs
from .test_suite_executor import execute_test_cases
from .custom_logger import CustomLogger
from .internal_path import INTERNAL_PATH
from .process_executor import APPIUM_PROPERTIES
