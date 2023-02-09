#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module is for storing path of project.
"""

from pathlib import Path
from os import listdir, name


class InternalPath:
    """Internal path container.

    This namespace stores all the path of every packages, files
    that will be used in execution progressing.
    """

    # Private consts to avoid changing
    __workspace_path = str(Path(__file__).parent.absolute().parent)
    __log_dir_path = f"{__workspace_path}/logs"
    __document_dir = f'{__workspace_path}/documentations'
    __test_case_dir = f'{__workspace_path}/test_cases'
    __latest_combined_log_path = f"{__log_dir_path}/latest_combined_log"
    __allure_bin_dir = f'{__workspace_path}/framework_modules/tools/allure/bin'

    __chromedriver_dir = \
        f'{__workspace_path}/framework_modules/tools/web_drivers'
    __chromedriver_mapping_file = \
        f'{__chromedriver_dir}/chrome_mapping_version.json'

    # Public var
    current_execution_log_dir = dict()

    @property
    def chromedriver_mapping_file(self) -> str:
        return self.__chromedriver_mapping_file

    @property
    def chromedriver_dir(self) -> str:
        return self.__chromedriver_dir

    @property
    def workspace_path(self) -> str:
        return self.__workspace_path

    @property
    def log_dir_path(self) -> str:
        return self.__log_dir_path

    @property
    def document_dir(self) -> str:
        return self.__document_dir

    @property
    def test_case_dir(self) -> str:
        return self.__test_case_dir

    @property
    def latest_combined_log(self) -> str:
        return self.__latest_combined_log_path

    @property
    def allure_bin(self) -> str:
        if name == 'nt':
            return f'{self.__allure_bin_dir}/allure.bat'
        return f'{self.__allure_bin_dir}/allure'

    @property
    def test_modules(self) -> dict:
        return {
            module_name: f"{self.__test_case_dir}/{module_name}"
            for module_name in listdir(self.__test_case_dir)
        }

    @property
    def current_allure_result_dir(self):
        return {
            key_: f"{value_}/allure-results"
            for key_, value_ in self.current_execution_log_dir.items()
        }

    @property
    def current_robot_report_dir(self) -> dict:
        return {
            key_: f"{value_}/robot"
            for key_, value_ in self.current_execution_log_dir.items()
        }

    @property
    def current_screenshot_dir(self) -> dict:
        return {
            key_: f"{value_}/screenshots"
            for key_, value_ in self.current_execution_log_dir.items()
        }

    @property
    def current_output_xml(self) -> dict:
        return {
            key_: f"{value_}/output.xml"
            for key_, value_ in self.current_robot_report_dir.items()
        }

    @property
    def current_syslog_robot_path(self) -> dict:
        return {
            key_: f"{value_}/syslog.txt"
            for key_, value_ in self.current_robot_report_dir.items()
        }

    @property
    def current_robot_log_file(self) -> dict:
        return {
            key_: f"{value_}/log.html"
            for key_, value_ in self.current_robot_report_dir.items()
        }

    def test_suites_of_module(self, module_name: str) -> dict:
        if module_name in self.test_modules:
            return {
                suite_name.replace(".robot", ""):
                    f"{self.test_modules.get(module_name)}/{suite_name}"
                for suite_name in listdir(self.test_modules.get(module_name))
            }
        return {}


INTERNAL_PATH = InternalPath()
