""" This module holds all constants that are used in the application"""

from flaskmicro.model import errors

APPLICATION_JSON = "application/json"

JSON_CONTENT = "application/json"

BEARER = "Bearer "

AUTHORIZATION = "Authorization"

DOCS_ROUTE = "/flask-micro-service"

URL_PREFIX = "/flask-micro/"

AUTH_API = f"{URL_PREFIX}auth"

API_SPECS_ROUTE = f"{DOCS_ROUTE}/openapi.json"

DESCRIPTION = (
   "Description"
)

INSECURE_APIS = [f"{URL_PREFIX}health"]

ERROR_RESPONSES = {
    "401": errors.UnAuthorizedError,
    "422": errors.PayloadError,
    "500": errors.InternalServerError,
    "503": errors.DBConnectionError,
}

OPENAPI_SECURITY = [{"jwt": []}]

ID_COLUMN_LENGTH = 999_999_999

UNSUPPORTED_CHARACTERS_ERROR_MSG = "query field contains unsupported characters"
