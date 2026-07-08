from sqlalchemy import Depends, select
from fastapi import HTTPException

from database.session import get_db
from models.student import Student

db = Depends(get_db)

def create_student(data):
    db.add(data)
    
    
    
    db.commit()
    
    db.refresh()
    
def get_all_students():
    query = select(Student)
    
    result = db.execute(query).scalars().all()
    
    return result

def get_student_by_id():
    query = select(Student).where(Student.id == 1)
    
    result = db.execute(query).scalar()
    
    return result

def update_student():
    query = select(Student).where(Student.id == 1)
    
    student = db.execute(query).scalar()
    
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    student.age = 18
    
    db.commit()
    
    db.refresh(student)
    
def delete_student():
    query = select(Student).where(Student.id == 1)
    
    student = db.execute(query).scalar()
    
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    
    db.delete(student)
    
    db.commit()
    
    db.refresh(student)