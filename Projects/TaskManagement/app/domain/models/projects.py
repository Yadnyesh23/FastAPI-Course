import uuid
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, ForeignKey, Uuid, Text

from app.database.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id : Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
        )
    title : Mapped[str] = mapped_column(
        String,
        nullable=False
        )
    description : Mapped[str]= mapped_column(
        Text
        )

    user_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
        )
    
    # relationship
    user : Mapped["User"] = relationship(
        "Student",
        back_populates="projects"
    )
    tasks : Mapped[list["Task"]]= relationship(
        back_populates="project"
    )
    