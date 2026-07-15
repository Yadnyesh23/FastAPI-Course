import uuid
from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import String, Uuid

from app.database.database import Base


class User(Base):
    __tablename__ = "users"
    
    id : Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        )
    name : Mapped[str] = mapped_column(
        String,
        nullable=False
        )
    
    email : Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True
        )
    
    # relationship
    projects : Mapped[list["Project"]] = relationship(
        back_populates="user"
      )