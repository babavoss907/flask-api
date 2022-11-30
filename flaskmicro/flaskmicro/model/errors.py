""" This module contains Pydantic Error Models"""

from typing import List

from pydantic import BaseModel, UUID4, create_model


class InvalidCredentials(BaseModel):
    msg: str
    request_id: UUID4


class BadRequest(InvalidCredentials):
    pass


class PayloadError(InvalidCredentials):
    msg: List[create_model("customError", field=(str, ...), error=(str, ...))]


class UnAuthorizedError(InvalidCredentials):
    pass


class InternalServerError(InvalidCredentials):
    pass


class DBConnectionError(InvalidCredentials):
    pass


class ResourceDoesNotExist(InvalidCredentials):
    pass


class UnsupportedPayload(InvalidCredentials):
    pass
