import uuid
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, Uuid, Text, Enum, ForeignKey

from app.database.database import Base
from app.domain.enums.db import TaskStatus

class Task(Base):
    __tablename__="tasks"
    
    id : Mapped[uuid.UUID]= mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
        )
    
    title = mapped_column(
        String,
        nullable=False
        )
    
    description : Mapped[str] = mapped_column(
        Text
        )
    status : Mapped[TaskStatus]= mapped_column(
        Enum(TaskStatus),
        nullable=False
        )
    project_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )
    
    # relationship
    project = relationship(
        "Project",
        back_populates="tasks"
    )