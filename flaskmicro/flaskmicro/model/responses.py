""" This module contains all the Pydantic response models"""
from pydantic import BaseModel


class AuthResponse(BaseModel):
    access_token: str


class DBHealthCheckResponse(BaseModel):
    __root__: str = "Alive!"


class TestAPP(BaseModel):
    test: str