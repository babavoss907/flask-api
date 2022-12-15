""" This module contains all configurations of this project"""
import logging
from os import getenv
from sys import exit
from typing import Optional
from uuid import uuid4

from flask import request
from flask_jwt_extended import verify_jwt_in_request
from flask_openapi3 import OpenAPI
from pydantic import BaseSettings, validator, Field, ValidationError

from flaskmicro.common.constants import INSECURE_APIS, DOCS_ROUTE, AUTH_API
# from flaskmicro.database import get_primary_session
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

    # Primary DB Configurations
    DB_HOST: str
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_PORT: int = Field(..., minimum_digits=4)

    # Common DB Configurations
    DB_POOL_SIZE: int = Field(..., minimum_digits=1)
    DB_MAX_OVERFLOW: int = Field(..., minimum_digits=1)

    class Config:
        min_anystr_length = 3
        anystr_strip_whitespace = True

    _validate_db_port = validator("DB_PORT", allow_reuse=True)(count_digits)
    _validate_db_pool_size = validator("DB_POOL_SIZE", allow_reuse=True)(count_digits)
    _validate_db_max_overflow = validator("DB_MAX_OVERFLOW", allow_reuse=True)(count_digits)


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

        # Adding user details to request object
        request.context |= dict(
            username='root',
            user_idn=2,
            loggedin_user_idn=2,
        )
