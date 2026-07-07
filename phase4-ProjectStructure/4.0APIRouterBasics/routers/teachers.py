from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)

class Teacher(BaseModel):
    name : str
    subject : str
    age : int

@router.get('/')
def get_teacher():
    return {
        "name" : "kevin",
        "subject" : "python",
        "age" : 20
    }
    
@router.post('/')
def create_teacher(teacher : Teacher):
    return {
        "data" : teacher
    }