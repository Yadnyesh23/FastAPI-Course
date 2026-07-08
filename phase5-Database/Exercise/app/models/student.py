from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column

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