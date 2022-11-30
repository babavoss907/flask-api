""" This module contains error messages for the application"""

import logging

from flask import request, Response
from simplejson import dumps
from sqlalchemy.exc import SQLAlchemyError

from flaskmicro.common.constants import JSON_CONTENT

logger = logging.getLogger(__name__)


def global_errors(err):
    """This function logs the JWT error and returns the Flask Response object with the
    JSON representation of the msg with HTTP status code.

    Args:
        err: The error message
    Returns:
        Response: Flask Response object with the JSON representation of the msg with HTTP status code
    """
    status_code = 500
    if isinstance(err, SQLAlchemyError):
        err = (
            "Got some error while processing data, "
            "either you are sending wrong data or server lost database connection."
        )
        status_code = 503
    elif isinstance(err, ConnectionRefusedError):
        err = "Service is not up or Something went wrong while processing the request"
    else:
        err = "Something went wrong while processing the request"

    return print_log_and_return_msg_with_request_id(err, status_code)


def missing_token_callback(err):
    """This function logs the JWT error and returns the Flask Response object with the
    JSON representation of the msg with HTTP status code.

    Args:
        err: The error message
    Returns:
        Response: Flask Response object with the JSON representation of the msg with HTTP status code
    """
    return print_log_and_return_msg_with_request_id("Authentication required", 401)


def validation_error(err):
    """This function logs the Pydantic validation error and returns the JSON representation of the msg with request_id.

    Args:
        err (list | dict): The Pydantic validation error
    Returns:
        JSON: the JSON representation of the msg with request_id
    """
    error = err
    if isinstance(err, dict) and (msg := err.get("msg")):
        error = msg
    elif isinstance(err, list):
        ordinal_numbers = {0: "1st", 1: "2nd", 2: "3rd"}
        error = [
            dict(
                field=f"{ordinal_numbers.get(e['loc'][1], str(e['loc'][1]) + 'th')} item in {e['loc'][0]}"
                if len(e["loc"]) > 1
                else e["loc"][0],
                error=e["msg"],
            )
            for e in err
        ]

    logger.error(err)
    return dumps({"msg": error, "request_id": request.context["request_id"]})


def http_errors(err):
    """This function logs the HTTP error and returns the Flask Response object with the
    JSON representation of the msg with HTTP status code.

    Args:
        err (HTTPError): The HTTP error message
    Returns:
        Response: Flask Response object with the JSON representation of the msg with HTTP status code
    """
    return print_log_and_return_msg_with_request_id(err.description, err.code)


def print_log_and_return_msg_with_request_id(msg, status_code):
    """This function log the msg and return the Flask Response object with the
    JSON representation of the msg with the given err_code.

    Args:
        msg (str): The message to logged and return in JSON format.
        status_code (int): The error code returned
    Returns:
        Response: Flask Response object with the JSON representation of the msg with the given err_code
    """
    logger.exception(msg)
    data = {"msg": msg, "request_id": request.context["request_id"]}
    return Response(dumps(data), status=status_code, content_type=JSON_CONTENT)
