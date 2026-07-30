from pydantic import BaseModel

class RegisterUserRequestModel(BaseModel):
    username: str
    email: str
    password: str

class LoginUserRequestModel(BaseModel):
    email: str
    password: str