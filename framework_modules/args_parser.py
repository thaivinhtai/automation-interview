#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module gets arguments via specified flags.
"""


import argparse


def __get_args() -> argparse.Namespace:
    """Get test arguments.

    Returns
    -------
    argparse.Namespace
        browser : browser to execute test on
        mobile_device : device to test on
        mobile_platform : {iOS, Android}
        mobile_platform_ver : mobile platform version
        app : The path to a .ipa, .apk or .zip file containing the app to test
        debug : Use when debugging, when this flag is enable the
                test cases won't re-run on failure.
        stop_on_failure : Immediately stop the script when failure is happened
        retry_times : The amount of times to be re-run when test cases failed,
                      default = 3.
        run_allure : Start allure reporting server after test.
        headless : Run browser in headless mode.
    """
    parser = argparse.ArgumentParser(description='Test Execution arguments '
                                                 'handling')
    parser.add_argument('-m', '--module', required=False, nargs="*",
                        default=['all'],
                        help='{api, mobile, web, all}')
    parser.add_argument('-t', '--tags', required=False, nargs='*',
                        help='Identifier of test cases to be run')
    parser.add_argument('--browser', required=False,
                        default='chrome', help='Browser to be run')
    parser.add_argument('--device-name', required=False,
                        help='Device to run test cases for mobile apps')
    parser.add_argument('--mobile-platform-ver', required=False,
                        help='Version of platform OS')
    parser.add_argument('--app', required=False,
                        help='The path to a .ipa, .apk or .zip '
                             'file containing the app to test.')
    parser.add_argument('--run-allure', required=False, action='store_true',
                        help='Run Allure report server in local')
    parser.add_argument('--appium-port', required=False, default='4723',
                        help='Specify port to run appium')
    parser.add_argument('--debug', required=False, action="store_true",
                        help="Use when debugging, when this flag is enable, "
                             "the test cases won't re-run on failure.")
    parser.add_argument('--stop-on-failure', required=False,
                        action="store_true", help=
                        "Immediately stop the script when failure is happened")
    parser.add_argument('--retry-times', required=False, default=1,
                        help="The amount of times to be re-run when test cases"
                             "failed, default=3")
    parser.add_argument('--gen-doc', required=False, action='store_true',
                        help='Generate test case documentation')
    return parser.parse_args()


# This global variable stores value of __get_args(), this makes ArgumentParser
# be initialed just one time and store the argparse.Namespace that we can use
# later.

ARGUMENTS = __get_args()
