from pydantic import BaseModel

class RegisterUserResponseModel(BaseModel):
    username : str
    email : str
    access_token : str
    token_type : str

class LoginUserResponseModel(BaseModel):
    access_token : str
    token_type : str
    