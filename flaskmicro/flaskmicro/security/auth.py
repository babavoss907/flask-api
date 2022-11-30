""" This module contains Authentication related business logic """
from functools import wraps
from secrets import compare_digest
from uuid import uuid4

from flask import current_app, Response
from flask_jwt_extended import create_access_token
from flask_openapi3 import APIBlueprint, Tag
from simplejson import dumps

from flaskmicro.common.constants import AUTH_API, JSON_CONTENT
from flaskmicro.common.exceptions import AuthorizationFailedError
from flaskmicro.model import payload as pld, errors, responses

auth_routes = APIBlueprint(
    "auth_APIs",
    __name__,
    abp_tags=[Tag(name="Authentication", description="Authentication API")],
    abp_responses={"400": errors.BadRequest, "401": errors.InvalidCredentials, "422": errors.PayloadError},
)


@auth_routes.post(AUTH_API, responses={"200": responses.AuthResponse})
def authenticate(body: pld.AuthBody):
    """Authentication API
    Return access token if the user is authenticated, else return 'Invalid credentials' with 401 code
    """
    result = UserAuthentication().authenticate(body)
    return Response(dumps(result), status=200, content_type=JSON_CONTENT)


class UserAuthentication:
    """This class contains the functions to generate Access Token"""

    def __init__(self):
        self.roles = (
            "ADMIN",
        )
        self.user_idn = 2

    def authenticate(self, payload: pld.AuthBody) -> dict:
        """This function authenticate the username and password and return JWT token with status code

        Args:
            payload (AuthBody): AuthBody object
        Returns:
            dict: a dict value with access_token key
        Raises:
            AuthorizationFailedError: if credentials doesn't match
        """

        app_username = current_app.config["APPLICATION_USERNAME"]
        app_password = current_app.config["APPLICATION_PASSWORD"]

        if payload.username == app_username and compare_digest(payload.password, app_password):
            user_claims = {"user_claims": {"roles": self.roles, "user_idn": self.user_idn}, "identity": app_username}
            access_token = create_access_token(identity=str(uuid4()), additional_claims=user_claims)
            return dict(access_token=access_token)
        raise AuthorizationFailedError("Invalid credentials")
