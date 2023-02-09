#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module handles test cases execution.
"""

from shutil import copyfile

from .args_parser import ARGUMENTS
from .internal_path import INTERNAL_PATH
from .log_dirs_generator import generate_current_time_execution_log_dir
from .process_executor import run_android_emulator, run_appium_server, \
    execute_robot_test_cases, create_latest_combined_log, \
    run_allure_report_server
from .env_vars_setup import set_robot_syslog_file_env_var


def execute_test_cases() -> None:
    """Execute test cases.

    This function gets arguments and calls module process_executor to run test
    cases.

    Returns
    -------
    None
    """

    generate_current_time_execution_log_dir()

    test_module_in_lower = [test_module.lower()
                            for test_module in list(set(ARGUMENTS.module))]
    if 'all' in test_module_in_lower:
        test_module_in_lower = INTERNAL_PATH.test_modules

    emulator_session = None
    appium_session = None
    appium_log = None

    for test_module in [module.lower() for module in test_module_in_lower
                        if module.lower() in INTERNAL_PATH.test_modules]:
        if test_module == "mobile":
            emulator_session = run_android_emulator(
                device_name=ARGUMENTS.device_name
            )
            appium_session, appium_log = run_appium_server(test_module)

        set_robot_syslog_file_env_var(
            INTERNAL_PATH.current_syslog_robot_path.get(test_module)
        )

        execute_robot_test_cases(
            debug=ARGUMENTS.debug, retry_times=ARGUMENTS.retry_times,
            stop_on_failure=ARGUMENTS.stop_on_failure, test_module=test_module
        )

        if test_module == "mobile":
            if appium_log and appium_session:
                appium_log.flush()
                appium_session.terminate()
                appium_session.wait()
                appium_log.close()
                copyfile(
                    f'{INTERNAL_PATH.current_execution_log_dir[test_module]}'
                    f'/appium-{ARGUMENTS.appium_port}.log',
                    f'{INTERNAL_PATH.latest_combined_log}'
                    f'/appium-{ARGUMENTS.appium_port}.log'
                )
            if emulator_session:
                emulator_session.terminate()
                emulator_session.wait()
                emulator_session.kill()

    # Export latest combined logs
    create_latest_combined_log()

    if ARGUMENTS.run_allure:
        allure_local_session = run_allure_report_server()
        input("Press any key to end the Allure report session.")
        allure_local_session.terminate()
        allure_local_session.wait()
