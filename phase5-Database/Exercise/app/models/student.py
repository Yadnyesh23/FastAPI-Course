from sqlalchemy import Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from database.base import Base

class Student(Base):
    __tablename__ ='students'
    
    id = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    
    name = mapped_column(
        String,
        nullable=False
    )
    
    email = mapped_column(
        String,
        unique=True,
        index=True
    )
    
    age = mapped_column(
        Integer
    )
    
    is_active = mapped_column(
        Boolean,
        default=True
    )
    
    notes = relationship(
        "Notes",
        back_populates="students"
    )
    
class Notes(Base):
    __tablename__ = "notes"
    
    id = mapped_column(
        Integer,
        unique=True,
        primary_key=True,
        autoincrement=True,
    )
    
    title = mapped_column(
        String,
    )
    
    content = mapped_column(
        Text
    )
    
    student_id = mapped_column(
        ForeignKey("students.id")
    )
    
    student = relationship(
        "Student",
        back_populates="notes"
    )