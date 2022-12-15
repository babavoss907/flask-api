"""
This is the main module. It contains all the configurations needed and Blueprints of all the APIs,
which are required to start the application.
"""
import os
from datetime import timedelta
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException
from flask_openapi3 import Info, HTTPBearer, OpenAPI

from flaskmicro.common import constants
from flaskmicro import config, error_handlers
from flaskmicro.routes.author_routes import author_routes


def create_app(flask_config=None):
    """Instantiation and configure of flask application

    Args:
        flask_config (str): Flask configuration value
    Returns:
        OpenAPI: Flask OpenAPI instance
    """
    info = Info(title=os.getenv("PROJECT_NAME"), version="1.0.0", description=constants.DESCRIPTION)
    app = OpenAPI(
        __name__,
        info=info,
        doc_prefix=constants.DOCS_ROUTE,
        api_doc_url=constants.API_SPECS_ROUTE,
        security_schemes={"jwt": HTTPBearer()},
    )

    # Load application configuration from the object
    config.LoadApplicationConfig(app, flask_config)

    # JSON Web Token configuration
    jwt = JWTManager(app)
    app.config["JWT_IDENTITY_CLAIM"] = "jti"
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "aptn"
    app.config["JWT_ACCESS_CSRF_HEADER_NAME"] = "X-CSRFT"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

    # Register Error Handlers
    jwt.unauthorized_loader(error_handlers.missing_token_callback)
    app.register_error_handler(HTTPException, error_handlers.http_errors)
    app.register_error_handler(Exception, error_handlers.global_errors)

    # Register blueprints
    app.register_api(author_routes)

    # Before request handlers
    app.before_request(config.before_request_func)

    return app
