from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get('/students/{id}', status_code=200)
def get_students(id : int):
    if id > 5:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "name" : "...",
        "email" : "...",
        "age" : "...",
    }

class Student(BaseModel):
    name : str 
    email : str
@app.post('/students', status_code=201)
def create_student(student : Student):
    return student