from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped
import uuid
from uuid import UUID
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP, DateTime
from datetime import datetime

class UserModel:
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    username : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    email : Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    password : Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    created_at : Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        default=func.now(),
        nullable=False
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    