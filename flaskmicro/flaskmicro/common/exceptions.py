""" This module contains all custom exception classes"""

from werkzeug.exceptions import HTTPException


class AuthorizationFailedError(HTTPException):
    code = 401

    def __init__(self, message):
        super(AuthorizationFailedError, self).__init__(message)


class UnSupportedQueryParams(HTTPException):
    code = 400

    def __init__(self, message):
        super(UnSupportedQueryParams, self).__init__(message)


class InternalServerError(HTTPException):
    code = 500

    def __init__(self, message):
        super(InternalServerError, self).__init__(message)  # pragma: no cover


class LimitValueNotSupported(HTTPException):
    code = 400

    def __init__(self, message):
        super(LimitValueNotSupported, self).__init__(message)


class OffsetValueNotSupported(HTTPException):
    code = 400

    def __init__(self, message):
        super(OffsetValueNotSupported, self).__init__(message)


class DBConnectionError(HTTPException):
    code = 503

    def __init__(self, message):
        super(DBConnectionError, self).__init__(message)


class UnSupportedQueryParamsValue(HTTPException):
    code = 400

    def __init__(self, message):
        super(UnSupportedQueryParamsValue, self).__init__(message)


class InsufficientQueryParams(HTTPException):
    code = 400

    def __init__(self, message):
        super(InsufficientQueryParams, self).__init__(message)


class ResourceDoesNotExist(HTTPException):
    code = 404

    def __init__(self, message):
        super(ResourceDoesNotExist, self).__init__(message)
