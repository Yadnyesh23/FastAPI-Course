from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

class Student(BaseModel):
    name : str
    age : int
    
@router.get('/')
def get_student():
    return {
        "name": "Yadnyesh",
        "age" : 20
    }

@router.post('/')
def create_student(student : Student):
    return {
        "data" : student
    }