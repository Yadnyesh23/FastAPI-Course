from fastapi import APIRouter, Depends
from pydantic import BaseModel

def verify_user():
    print("User Verified")
    
router = APIRouter(
    prefix="/students",
    tags=["Students"],
    dependencies=[Depends(verify_user)]
)

class Student(BaseModel):
    name: str
    age : int
@router.get('/')
def get_student():
    return {
        "data" : "student data"
    }
    
@router.post('/', status_code=201)
def create_student(student : Student):
    return student
