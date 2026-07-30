# app/domain/schemas/request/auth.py

from pydantic import BaseModel, EmailStr


class LoginRequestModel(BaseModel):
    email: EmailStr
    password: str