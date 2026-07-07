from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, field_validator

app = FastAPI()

class Address(BaseModel):
    city : str
    state : str
    
class UserResponse(BaseModel):
    username : str
    email : str
    address : Address
    
@app.get('/students', response_model=list[UserResponse])
def get_user():
    return [{
    "username": "...",
    "email": "...",
    "password": "secret",
    "address" : {
        "city" : "...",
        "state" : "..."
    }
    },
            {
    "username": "...",
    "email": "...",
    "password": "secret",
    "address" : {
        "city" : "...",
        "state" : "..."
    }
    }]
    
# Accept username, email, password in request but dont show password in response , just show username and email

class Student(BaseModel):
    username : str
    email : str
    password : str
    
    @field_validator("username")
    @classmethod
    def username_validate(cls, value):
        if value == "string":
            raise ValueError("String username is not allowed.")
        return value

class StudentResponse(BaseModel):
    username : str
    email : str
    
@app.post('/students', response_model=StudentResponse)
def create_student(student : Student):
    return student