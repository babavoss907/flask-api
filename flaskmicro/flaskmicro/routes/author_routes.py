from flask import Response
import flaskmicro.model.responses as res
from flask_openapi3 import APIBlueprint, Tag
from flaskmicro.resources.authors import Controller
from flaskmicro.common.constants import JSON_CONTENT, ERROR_RESPONSES, OPENAPI_SECURITY, URL_PREFIX
import flaskmicro.model.payload as payload


app_test = [Tag(name="App Test | Test", description="Test API and DB")]
app_test_post_query = [Tag(name="DB Check | Test", description="Test Insert & Query")]

author_routes = APIBlueprint(
    "add_APIs",
    __name__,
    url_prefix=URL_PREFIX,
    abp_responses=ERROR_RESPONSES,
    abp_security=OPENAPI_SECURITY,
)


@author_routes.get("/test-db", tags=app_test, responses={'200':res.TestAPP})
def get_test_db():
    """
    test API
    """
    flaskmicro = Controller()
    data = flaskmicro.get_test_db()
    return Response(data, status=200, content_type=JSON_CONTENT)

@author_routes.get("/test-db-query", tags=app_test_post_query, responses={'200':res.TestAPP})
def test_db_query_last_name(query:payload.GetAuthorByLastName):
    """
    test API query
    """
    flaskmicro = Controller()
    data = flaskmicro.get_test_db_query(query)
    return Response(data, status=200, content_type=JSON_CONTENT)

@author_routes.post("/test-db-insert", tags=app_test_post_query, responses={'200':res.TestAPP})
def get_test_insert(body:payload.SaveAuthor):
    """
    test API post
    """
    flaskmicro = Controller()
    data = flaskmicro.get_test_db_insert(body)
    return Response(data, status=201, content_type=JSON_CONTENT)

