from pydantic import BaseModel

class RegisterResponse(BaseModel):
    message:str
    user:dict

class LoginResponse(BaseModel):
    message:str
    access_token:str
    refresh_token:str
    token_type: str = "bearer"

class RefreshTokenResponse(BaseModel):
    message: str
    access_token: str
    token_type: str = "bearer"