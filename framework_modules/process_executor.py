#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module handles call to other processes.

    Functions in this module:

        +   execute_robot_test_cases(*args) -> None
                Execute robot test cases.

        +   generate_allure_report() -> None
                Generate allure report

        +   run_allure_report_server() -> None
                Open Allure report.

        +   run_appium_server() -> Popen
                Run Appium server.

        +   run_android_emulator(name: str) -> Popen
                Run Android emulator

        +   push_result() -> None
                Push execution results to report sever.
"""

from os import kill, environ, system, listdir, path, name, mkdir, remove

if name == "posix":
    from os import O_NONBLOCK
    import fcntl

from signal import SIGTERM
from subprocess import Popen, PIPE, run
from time import sleep
from sys import stdout
from shutil import copyfile, rmtree
from requests import request
from requests.exceptions import ConnectionError, ConnectTimeout

from typing import Union

from allure_robotframework import allure_robotframework
from robot import run as robot_run, rebot
from .internal_path import INTERNAL_PATH
from .args_parser import ARGUMENTS


class AppiumProperties:

    def __init__(self, port: int = 4723):
        self.port = port
        self.mobile_udid = ""
        self.chrome_driver_port = self.port + 2000
        self.mjpeg_server_port = self.port + 3000
        self.system_port = self.port + 4000

    def get_appium_port(self):
        return self.port

    def get_mobile_udid(self):
        return self.mobile_udid

    def get_chrome_driver_port(self):
        return self.chrome_driver_port

    def get_mjpeg_server_port(self):
        return self.mjpeg_server_port

    def get_system_port(self):
        return self.system_port


APPIUM_PROPERTIES = AppiumProperties(int(ARGUMENTS.appium_port))


def check_appium_session(port: int) -> dict:
    """Check appium session.

    This function checks if appium server is running and there is session here.

    Returns
    -------
    dict
        appium_server : bool
        available_session : bool
    """
    available_session = False
    appium_server = False
    try:
        response = request(
            method='GET', timeout=1,
            url=f'http://127.0.0.1:{port}/wd/hub/sessions')
        if response.status_code == 200:
            appium_server = True
        if response.json().get('value'):
            available_session = True
        return {'appium_server': appium_server,
                'available_session': response.json().get('value')}
    except (ConnectTimeout, ConnectionError):
        pass
    return {'appium_server': appium_server,
            'available_session': available_session}


def print_progress_bar(wait_time: float, progress_status: str,
                       done: bool = False) -> None:
    """Print progress bar.

    This function visible the progress on console.

    Parameters
    ----------
    wait_time : float
        total time to wait.
    progress_status : str
        Status of the process.
    done : bool
        If done, progress bar shows 100%
    """

    def progress_bar(count: int, total: float, status: str):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        stdout.flush()

    increase = 0.01
    total_progress = wait_time / increase
    counter = 0
    while counter < total_progress:
        if done:
            counter = total_progress
        progress_bar(counter, total_progress, progress_status)
        sleep(increase)  # emulating long-playing job
        counter += 1


def execute_robot_test_cases(test_module: str, debug: bool = False,
                             retry_times: int = 1,
                             stop_on_failure: bool = False) -> None:
    """Execute robot test cases.

    This function call robot as sub-subprocess, execute robot test cases and
    export log.

    Parameters
    ----------
    test_module : str
        Test module: api, web, mobile
    debug : bool
        True to debug.
    retry_times : int
        The amount of times to retry test cases when they are failed.
    stop_on_failure : Immediately stop the test script.

    Returns
    -------
    None
    """

    class LogToConsoleAndFile:
        @staticmethod
        def flush():
            stdout.flush()
            open(
                INTERNAL_PATH.current_execution_log_dir.get(test_module)
                + '/execution.log', 'a+'
            ).flush()

        @staticmethod
        def write(text):
            execution_log = open(
                INTERNAL_PATH.current_execution_log_dir.get(test_module)
                + '/execution.log', 'a+'
            )
            execution_log.write(text)
            stdout.write(text)

    log_level = "INFO:INFO"
    if debug:
        log_level = "TRACE:TRACE"

    robot_run(
        INTERNAL_PATH.test_modules.get(test_module), loglevel=log_level,
        listener=allure_robotframework(
            INTERNAL_PATH.current_allure_result_dir.get(test_module)
        ), outputdir=INTERNAL_PATH.current_robot_report_dir.get(test_module),
        stdout=LogToConsoleAndFile, stderr=LogToConsoleAndFile,
        exitonfailure=stop_on_failure, exitonerror=stop_on_failure,
        log=f'{INTERNAL_PATH.current_robot_log_file.get(test_module)}',
        output=f'{INTERNAL_PATH.current_output_xml.get(test_module)}',
        consolecolors="on", variable=[f"TEST_MODULE:{test_module}"]
    )

    if not debug and not stop_on_failure:
        if retry_times > 0:
            copyfile(
                f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
                f'/output.xml',
                f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
                f'/output-0.xml'
            )
        for i in range(retry_times):
            robot_run(
                INTERNAL_PATH.test_modules.get(test_module),
                loglevel=log_level,
                listener=
                allure_robotframework(
                    INTERNAL_PATH.current_allure_result_dir.get(test_module)),
                outputdir=
                INTERNAL_PATH.current_robot_report_dir.get(test_module),
                stdout=LogToConsoleAndFile, stderr=LogToConsoleAndFile,
                log=
                f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
                f'/log-rerun-{i + 1}.html',
                rerunfailed=
                f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
                f'/output-{i}.xml',
                output=
                f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
                f'/output-{i +  1}.xml',
                consolecolors="on"
            )

    # Collect all output file after run
    list_output_file = []
    for file_ in listdir(
            INTERNAL_PATH.current_robot_report_dir.get(test_module)):
        if file_.startswith('output'):
            list_output_file.append(
                f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
                f'/{file_}'
            )

    # Merge all the output
    rebot(output=f'{INTERNAL_PATH.current_output_xml.get(test_module)}',
          log=f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
              f'/log-final.html',
          report=
          f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
          f'/report-final.html',
          merge=True, *list_output_file)

    # Remove redundant output file
    list_output_file.remove(
        f'{INTERNAL_PATH.current_robot_report_dir.get(test_module)}'
        f'/output.xml'
    )
    [remove(file_) for file_ in list_output_file]


def create_latest_combined_log() -> None:
    """Create latest combined log.

    Combine all output.xml from all current execution suite in to one xml.

    Returns
    -------
    None
    """

    if not path.exists(INTERNAL_PATH.latest_combined_log):
        mkdir(INTERNAL_PATH.latest_combined_log)

    if path.exists(f"{INTERNAL_PATH.latest_combined_log}/robot"):
        rmtree(f"{INTERNAL_PATH.latest_combined_log}/robot")

    mkdir(f"{INTERNAL_PATH.latest_combined_log}/robot")
    rebot(output=f'{INTERNAL_PATH.latest_combined_log}/robot/output.xml',
          log=f'{INTERNAL_PATH.latest_combined_log}/robot/log.html',
          report=f'{INTERNAL_PATH.latest_combined_log}/robot/report.html',
          xunit=f'{INTERNAL_PATH.latest_combined_log}/robot/report.xml',
          *INTERNAL_PATH.current_output_xml.values())
    collect_current_allure_result_and_generate_report()


def _get_all_result_files_in_current_execution() -> tuple:
    """Get all result files in current execution.

    This function gets all files name and their absolute path of Allure result
    in current execution time.

    Returns
    -------
    tuple
        (result_files - list of absolute path to files,
         files - list name of files)
    """
    result_dir = INTERNAL_PATH.current_allure_result_dir.values()

    result_files = list()
    files = list()
    for directory in result_dir:
        files += [file for file in listdir(directory)]
        result_files += [f'{directory}/{file}' for file in listdir(directory)]
    return result_files, files


def collect_current_allure_result_and_generate_report() -> None:
    """Collect current Allure result and generate report.

    Collect all the Allure result, copy it to temp folder and then generate
    Allure report.

    Returns
    -------
    None
    """
    if not path.exists(f"{INTERNAL_PATH.latest_combined_log}/allure"):
        mkdir(f"{INTERNAL_PATH.latest_combined_log}/allure")

    temp_allure_result = (f"{INTERNAL_PATH.latest_combined_log}"
                          f"/allure/result")
    temp_allure_report = (f"{INTERNAL_PATH.latest_combined_log}"
                          f"/allure/report")

    if path.exists(temp_allure_result):
        rmtree(temp_allure_result)

    result_files, files = _get_all_result_files_in_current_execution()
    mkdir(temp_allure_result)

    for full_path, file_name in zip(result_files, files):
        copyfile(full_path, f"{temp_allure_result}/{file_name}")

    allure_local_generating = Popen(
        [INTERNAL_PATH.allure_bin, 'generate', temp_allure_result,
         '--output', temp_allure_report, '--clean'],
        env=environ
    )
    print_progress_bar(
        wait_time=3,
        progress_status=f"Generating Allure local report."
    )
    allure_local_generating.wait()


def run_allure_report_server() -> Popen:
    """Run Allure report server.

    This function run Allure server with the latest log information.

    Returns
    -------
    Popen
        allure session
    """
    temp_allure_report = f"{INTERNAL_PATH.latest_combined_log}/allure/report"

    allure_local_session = \
        Popen(
            [INTERNAL_PATH.allure_bin, 'open', temp_allure_report], env=environ
        )
    print_progress_bar(
        wait_time=2,
        progress_status=f"Starting Allure local report."
    )
    return allure_local_session


def run_appium_server(test_module: str) -> tuple:
    """Run Appium server.

    Call Appium sever.

    Parameters
    ----------
    test_module : str
        Test module: api, web, mobile

    Returns
    -------
    tuple
        Appium session, logfile
    """
    result = check_appium_session(APPIUM_PROPERTIES.port)
    if not result.get('appium_server'):
        try:
            free_port(APPIUM_PROPERTIES.port)
        except (ProcessLookupError, PermissionError) as error:
            raise Exception(f"Could not kill process using port "
                            f"{APPIUM_PROPERTIES.port}. {error}")
    if result.get('appium_server') and not result.get('available_session'):
        return None, None
    if result.get('available_session'):
        APPIUM_PROPERTIES.chrome_driver_port += \
            len(result.get('available_session'))
        APPIUM_PROPERTIES.mjpeg_server_port += \
            len(result.get('available_session'))
        APPIUM_PROPERTIES.system_port += \
            len(result.get('available_session'))
        return None, None
    appium_log_file = \
        f'{INTERNAL_PATH.current_execution_log_dir.get(test_module)}' \
        f'/appium-{APPIUM_PROPERTIES.port}.log'
    appium_log = open(appium_log_file, 'a')
    appium_log.flush()
    appium_command = ['appium']
    if name == "nt":
        appium_command = ['appium.cmd']
    appium_session = Popen([*appium_command, "--port",
                            str(APPIUM_PROPERTIES.port),
                            '--allow-insecure', 'chromedriver_autodownload'],
                           stdout=appium_log, stderr=appium_log, env=environ)

    print_progress_bar(
        wait_time=3,
        progress_status=f"Starting Appium server on port "
                        f"{APPIUM_PROPERTIES.port}."
    )
    while True:
        if 'Appium REST http interface listener started' in \
                open(appium_log_file).read():
            break
        sleep(1)
    return appium_session, appium_log


def get_attached_android_devices() -> list:
    """Get attached Android devices.

    Returns
    -------
    list
        list of attached devices name.
    """
    command = ['adb', 'devices']
    splitter = '\r'
    is_shell = True
    if name == 'nt':  # For Window 10 user
        command = ["cmd", "/c"] + command
        splitter = '\r\n'
    if name == 'posix':  # For MacOS user
        splitter = '\n'
        is_shell = False
    run(command)
    c = Popen(command, shell=is_shell, stdout=PIPE, stderr=PIPE)
    standard_out, _ = c.communicate()
    output = standard_out.decode().strip().split(splitter)
    output.pop(0)
    for index, line in enumerate(output):
        output[index] = line.replace(line[line.find('\t'):], "")
    return output


def get_available_emulators() -> list:
    """Get available emulator.

    Returns
    -------
    list
        list of available emulators.
    """
    command = ['emulator', '-list-avds']
    splitter = '\r'
    is_shell = True
    if name == 'nt':  # For window
        command = ["cmd", "/c"] + command
        splitter = '\r\n'
    if name == 'posix':  # For MacOS 12
        is_shell = False
        splitter = '\n'
    c = Popen(command, shell=is_shell, stdout=PIPE, stderr=PIPE)
    standard_out, _ = c.communicate()
    output = standard_out.decode().strip().split(splitter)
    return output


def get_emulators_real_name(list_devices: list) -> list:
    """Get emulators real name.

    Parameters
    ----------
    list_devices : list
        List of attached devices that is got from adb devices command.

    Returns
    -------
    list
        List of emulators with their real names.
    """

    command = ['adb', '-s', None, 'emu', 'avd', 'name']
    index = 2
    is_shell = True
    splitter = '\r\r\n'
    if name == 'nt':  # For Window user
        command = ["cmd", "/c"] + command
        index += 2
    if name == 'posix':  # For MacOS user
        is_shell = False
        splitter = '\r\n'
    emulator_names = []
    for device_name in list_devices:
        command[index] = device_name
        c = Popen(command, shell=is_shell, stdout=PIPE, stderr=PIPE)
        standard_out, _ = c.communicate()
        output = standard_out.decode().strip().split(splitter)[0]
        emulator_names.append(output)
    return emulator_names


def run_android_emulator(**kwargs) -> Union[Popen, None]:
    """Run Android emulator.

    Run an Android emulator base on provided name.

    Parameters
    ----------
    kwargs
        device_name : str
            Emulator name.
        debug : bool
            False for headless mode.

    Returns
    -------
    Union
        Android emulator session.
        None
    """
    emulator_name = kwargs.get("device_name")
    debug = kwargs.get("debug")
    attached_devices = get_attached_android_devices()
    emulators_real_name = get_emulators_real_name(attached_devices)
    running_devices = attached_devices + emulators_real_name
    emulator_udid = {
        name_: id_ for name_, id_ in zip(emulators_real_name, attached_devices)
    }
    if emulator_name in running_devices:
        APPIUM_PROPERTIES.mobile_udid = emulator_udid.get(emulator_name)
        return None
    if emulator_name not in get_available_emulators():
        print(r"\\          //  //\\  ||==|| ||\\  || == ||\\  || ====== ")
        print(r" \\  //\\  //  //==\\ ||==|| || \\ || || || \\ || ||  ===")
        print(r"  \\//  \\//  //    \\||   \\||  \\|| == ||  \\|| ||===||")
        print("==========================================================")
        print(f"The device/emulator {emulator_name} is not available.")
        print("==========================================================")
        return None
    print("===================================================")
    print(f"The device: {emulator_name} is not running")
    print("===================================================")
    command = ['emulator', '-avd', emulator_name]  # , '-no-snapshot']
    if name == 'nt':  # For window 10
        command = ["cmd", "/c"] + command
    # if not debug:
    #     command += ['-noaudio', '-no-boot-anim', '-no-window']
    emulator_session = Popen(command, stdout=PIPE)
    print_progress_bar(
        wait_time=10,
        progress_status=f"Starting emulator {emulator_name}."
    )
    timeout = 10
    while True:
        if name == "posix":  # For MacOS 12
            fd = emulator_session.stdout.fileno()
            fl = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | O_NONBLOCK)
        line = emulator_session.stdout.readline()
        line_in_string = line.rstrip().decode('utf-8')
        print(line_in_string)
        if "emulator: INFO: boot completed" in line_in_string:
            break
        if not line_in_string:
            break
        if timeout <= 0:
            break
        sleep(1)
        timeout += -1
    attached_devices = get_attached_android_devices()
    emulators_real_name = get_emulators_real_name(attached_devices)
    emulator_udid = {
        name_: id_ for name_, id_ in zip(emulators_real_name, attached_devices)
    }
    APPIUM_PROPERTIES.mobile_udid = emulator_udid.get(emulator_name)
    print("exit")
    return emulator_session


def free_port(port: int) -> None:
    """

    Parameters
    ----------
    port

    Returns
    -------

    """
    command = f"lsof -i :{port}"
    index = 9
    if name == 'nt':
        command = ["cmd", "/c", "netstat", "-ano", "|", "findstr", f"{port}"]
        index = 4
    c = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    standard_out, _ = c.communicate()
    output = standard_out.decode().strip().split(' ')
    while "" in output:
        output.remove("")
    try:
        pid = int(output[index])
        if name == 'nt':
            system(f'taskkill /f /im {pid}')
        else:
            kill(pid, SIGTERM)
    except IndexError:
        pass
    except TypeError as error:
        raise Exception(f"Could not kill process {output[9]}. {error}")
