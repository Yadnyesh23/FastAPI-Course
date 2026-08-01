from pydantic import BaseModel

class RegisterResponse(BaseModel):
    message:str
    user:dict

class LoginResponse(BaseModel):
    message:str
    access_token:str