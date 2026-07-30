# app/domain/schemas/response/auth.py

from pydantic import BaseModel
from uuid import UUID


class UserInfo(BaseModel):
    id: UUID
    name: str
    email: str


class LoginResponseModel(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user: UserInfo