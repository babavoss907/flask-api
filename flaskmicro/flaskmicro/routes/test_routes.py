from flask import Response
import flaskmicro.model.responses as res
from flask_openapi3 import APIBlueprint, Tag
from flaskmicro.resources.notification.letter import Controller
from flaskmicro.common.constants import JSON_CONTENT, ERROR_RESPONSES, OPENAPI_SECURITY, URL_PREFIX
import flaskmicro.model.payload as payload


app_test = [Tag(name="App Test | Test", description="Test API")]

test_routes = APIBlueprint(
    "add_APIs",
    __name__,
    url_prefix=URL_PREFIX,
    abp_responses=ERROR_RESPONSES,
    abp_security=OPENAPI_SECURITY,
)


@test_routes.get("/test-db", tags=app_test, responses={'200':res.TestAPP})
def get_test_db():
    """
    test API
    """
    add_letter = Controller()
    data = add_letter.get_test_db()
    return Response(data, status=200, content_type=JSON_CONTENT)

@test_routes.get("/test-db-query", tags=app_test, responses={'200':res.TestAPP})
def get_test_db_query(query:payload.GetAuthorByFirstName):
    """
    test API
    """
    add_letter = Controller()
    data = add_letter.get_test_db_query(query)
    return Response(data, status=200, content_type=JSON_CONTENT)

@test_routes.post("/test-db-insert", tags=app_test, responses={'200':res.TestAPP})
def get_test_insert(body:payload.SaveAuthor):
    """
    test API
    """
    add_letter = Controller()
    data = add_letter.get_test_db_insert(body)
    return Response(data, status=200, content_type=JSON_CONTENT)

# @letter_routes.get("/letter-job-listings", tags=gear_icon_tag, responses={"200": res.LoggedCorrespondenceDetailsResponse})
# # @has_permission('Ze Notification LoggedCorrespondenceDetails')
# def get_logged_correspondence_details(query:payload.LoggedCorrespondenceDetails):
#     """
#     correspondence view gear icon view log
#     """
#     add_letter = NotificationController()
#     data = add_letter.get_logged_correspondence_details(query)
#     return Response(data, status=200, content_type=JSON_CONTENT)


# @letter_routes.post("/add-letter", tags=add_letter_tag, responses={"201": res.SaveLetterResponse})
# # @has_permission('Ze Notification AddEpisodeNotification')
# def save_letter_prefills_member_level(body:payload.SaveLetter):
#     """
#     Save button on Add Letter screen
#     """
#     add_letter = NotificationController()
#     response = Response(add_letter.add_letter(body), status=201, content_type=JSON_CONTENT)
#     return response

