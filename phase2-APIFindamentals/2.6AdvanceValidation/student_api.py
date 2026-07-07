from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, field_validator

app = FastAPI()

class Student(BaseModel):
    name : str = Field(
        min_length=4,
        max_length=30
    )
    username : str = Field(
        pattern = r"^[a-zA-Z0-9_]+$"
    )
    age : int = Field(
        ge=18,
        le=30
    )
    email : EmailStr
    password : str
    
    @field_validator("password")
    @classmethod
    def validatePassword(cls, value):
        
        if len(value) < 8:
            raise ValueError("Password too short")
        
        return value
    
    
@app.post('/students')
def create_student(student: Student):
    return {
        "message" : "Student created succesfully",
        "data" : student
    }