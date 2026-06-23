from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    name : str
    age : int
    branch : str
    bio : str | None = None
    
    
@app.post('/students')
def create_students(student:Student):
    return {
        "message" : "Student Created",
        "data" : student
    }