from sqlalchemy import String, TIMESTAMP
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid
from sqlalchemy import Uuid


from app.db.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id : Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    name : Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    email : Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    password : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    created_at : Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at : Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )