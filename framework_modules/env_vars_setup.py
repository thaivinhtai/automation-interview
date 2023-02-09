#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains functions to setup environ variables for the project.

        Function in this module:

            +   set_python_path_env_var() -> None
                    Setup value for PYTHONPATH

            +   set_robot_syslog_file_env_var() -> None
                    Set value for ROBOT_SYSLOG_FILE

"""

from os import environ
from .internal_path import INTERNAL_PATH


def set_python_path_env_var() -> None:
    """Setup Python path environment variable.

    This function setup PYTHONPATH environment variable that's used for
    robot file to understand the import libraries in entire project.

    Returns
    -------
    None
    """
    environ['PYTHONPATH'] = INTERNAL_PATH.workspace_path


def set_robot_syslog_file_env_var(log_path: str) -> None:
    """Set Robot syslog file environ variable.

    This function set value for ROBOT_SYSLOG_FILE environ variable to specify
    path of robot syslog file, that will store log of system when running
    robot.

    Parameters
    ----------
    log_path : str
        Path to the folder to stare the robot syslog.

    Returns
    -------
    None
    """
    environ['ROBOT_SYSLOG_FILE'] = log_path
