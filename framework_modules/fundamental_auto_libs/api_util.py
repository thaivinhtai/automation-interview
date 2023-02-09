#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This module contains function for convenience.
"""

from requests import request
from json import dumps, JSONEncoder
from robot.libraries.BuiltIn import BuiltIn

from framework_modules import CustomLogger


CURRENT_TEST_NAME = BuiltIn().get_variable_value("${TEST_MODULE}")
LOGGER = CustomLogger(CURRENT_TEST_NAME)


class CustomJSONEncoder(JSONEncoder):
    pass


def make_beauty_json(json_data: dict) -> str:
    """Make beauty JSON.

    Transform JSON instance into readable form.

    Parameters
    ----------
    json_data : a dictionary or a JSON instance

    Returns
    -------
    str
    """
    return dumps(json_data, indent=4, sort_keys=True, cls=CustomJSONEncoder) \
        if type(json_data) in (dict, list) else json_data


def send_request_and_receive_response(method: str, uri: str, **kwargs) -> dict:
    """Send and receive request.

    This function sends and receives request then logs to console.

    Parameters
    ----------
    method : str
        HTTP method
    uri : str
        URI

    Returns
    -------
    dict
        {"message": , "status_code": }
    """
    headers = kwargs.pop('headers', {'Accept': '*/*'})
    body = kwargs.pop('body', {})

    beauty_headers = make_beauty_json(headers)
    beauty_body = make_beauty_json(body)
    LOGGER.debug("Request Headers: \n" + beauty_headers)
    LOGGER.debug("Request data: \n" + beauty_body)

    response = request(method, uri, headers=headers,
                       data=body, **kwargs)

    print('status: ', response.headers, response.content)
    response_message = response.json()
    beauty_response = make_beauty_json(response_message)
    status_code = response.status_code

    LOGGER.debug("Got response message: \n" + beauty_response)
    LOGGER.info("Status code: " + str(status_code))

    return {'message': response_message, 'status_code': status_code}
