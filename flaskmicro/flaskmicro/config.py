""" This module contains all configurations of this project"""
import logging
from os import getenv
from sys import exit
from typing import Optional, Literal
from uuid import uuid4

from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_openapi3 import OpenAPI
from pydantic import BaseSettings, validator, Field, ValidationError

from flaskmicro.common.constants import INSECURE_APIS, DOCS_ROUTE, AUTH_API
# from flaskmicro.database import get_primary_session
from flaskmicro.error_handlers import validation_error
from flaskmicro.model.validators import count_digits

logger = logging.getLogger(__name__)


class BasicConfig(BaseSettings):
    # Application Configurations
    PROJECT_NAME: str
    DEBUG: bool = False
    Testing: bool = False
    PROPAGATE_EXCEPTIONS: bool = True
    # FLASK_RUN_PORT: int = Field(..., minimum_digits=4)

    # Application Security Configurations
    JWT_SECRET_KEY: str

    # Other Configurations
    Environment: str
    # TEMP_FILE: str
    # EMAIL_SMTP_SERVER_NAME: str
    # EMAIL_SMTP_SERVER_PORT: int = Field(..., minimum_digits=2)
    # MS_CACHE_CONFIG_ENABLED: Literal["False", "True"] = "False"

    # Primary DB Configurations
    DB_HOST: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_PORT: int = Field(..., minimum_digits=4)

    # Secondary DB Configurations
    # SEC_DB_HOST: str
    # SEC_DB_NAME: str
    # SEC_DB_USERNAME: str
    # SEC_DB_PASSWORD: str
    # SEC_DB_PORT: int = Field(..., minimum_digits=4)

    # Common DB Configurations
    DB_POOL_SIZE: int = Field(..., minimum_digits=1)
    DB_MAX_OVERFLOW: int = Field(..., minimum_digits=1)

    class Config:
        min_anystr_length = 3
        anystr_strip_whitespace = True

    # _validate_flask_run_port = validator("FLASK_RUN_PORT", allow_reuse=True)(count_digits)
    _validate_db_port = validator("DB_PORT", allow_reuse=True)(count_digits)
    # _validate_sec_db_port = validator("SEC_DB_PORT", allow_reuse=True)(count_digits)
    _validate_db_pool_size = validator("DB_POOL_SIZE", allow_reuse=True)(count_digits)
    _validate_db_max_overflow = validator("DB_MAX_OVERFLOW", allow_reuse=True)(count_digits)
    # _validate_email_smtp_server_port = validator("EMAIL_SMTP_SERVER_PORT", allow_reuse=True)(count_digits)


class SecurityConfig(BasicConfig):
    APPLICATION_USERNAME: str
    APPLICATION_PASSWORD: str


class ProductionConfig(BasicConfig):
    FLASK_ENV: str = "production"


class TestingConfig(SecurityConfig):
    FLASK_ENV: str = "testing"
    Testing: bool = True


class DevelopmentConfig(SecurityConfig):
    FLASK_ENV: str = "development"
    DEBUG: bool = True


config_obj = {"production": ProductionConfig, "testing": TestingConfig, "development": DevelopmentConfig}


class LoadApplicationConfig:
    """This class takes app and flask config value to check if the provided configurations are sufficient to start
    the service, if not it will exit the service with an error message with the missing configurations.
    If all the configurations exist then the app will be updated with the configurations.
    Along with that, auth API will be made available based on the environment."""

    def __init__(self, app: OpenAPI, flask_config: Optional[str]):
        """This function will update the app with the given configurations and make
        auth available based on the environment

        Args:
            app (OpenAPI): The OpenAPI instance
            flask_config (str): The app environment configuration
        """
        if flask_config:
            config_name = flask_config.lower()
        else:
            config_name = getenv("FLASK_ENV", default="production")

        if config_name != "production":
            from flaskmicro.security.auth import auth_routes

            app.register_api(auth_routes)
            INSECURE_APIS.append(AUTH_API)

        try:
            app.config.update(config_obj[config_name]().dict())
        except ValidationError as err:
            logger.critical(
                f'Please provide valid values for ({", ".join(i["loc"][0] for i in err.errors())}) '
                f"environment variables, to spin up the service in {config_name} mode."
            )
            exit(4)


def before_request_func():
    """This function called before every request. Here we append the required details to the request object"""
    request.context = dict(request_id=request.headers.get("X-Request-ID", str(uuid4())))
    if DOCS_ROUTE not in request.path not in INSECURE_APIS:
        # Authentication
        verify_jwt_in_request()
        # user_details = get_jwt()
        # claims = user_details["user_claims"]

        # Adding user details to request object
        request.context |= dict(
            username='root',
            user_idn=2,
            loggedin_user_idn=2,
        )

        # Adding db session to request object
        # request.db_session = get_primary_session()


# def after_request_func(res):
#     """This function is called after the request. Here we look for 422 status code and modify the response date

#     Args:
#         res (Response): Response object
#     Response:
#         Response: Response object
#     """
#     if res.status_code == 201:
#         request.context["commit_db_transaction"] = True
#     elif res.status_code == 422:
#         res.data = validation_error(res.json)
#     return res


# def teardown_request_func(res):
#     """This function is called after the request. Here we close the session object

#     Args:
#         res (Response): Response object
#     Response:
#         Response: Response object
#     """
#     if hasattr(request, "db_session") and request.db_session:
#         if request.context.get("commit_db_transaction"):
#             request.db_session.commit()
#         else:
#             request.db_session.rollback()
#         request.db_session.close()
#     return res
