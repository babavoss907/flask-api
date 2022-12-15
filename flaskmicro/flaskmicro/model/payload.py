""" This  module contains all the Pydantic Models to validate the incoming request data"""

from pydantic import BaseModel, Field


class AuthBody(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=3)

class SaveAuthor(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    birthdate: str = Field(...)
    added: str = Field(...)

class GetAuthorByLastName(BaseModel):
    last_name: str = Field(...)