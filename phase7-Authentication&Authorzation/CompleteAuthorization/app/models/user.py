
import uuid
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import DateTime, String

from app.database.db import Base


class UserModel(Base):
    __tablename__ = 'users'

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True, 
        default=uuid.uuid4
        )
    username : Mapped[str] = mapped_column(
        String(15), 
        unique=True, 
        nullable=False
        )
    email : Mapped[str] = mapped_column(
        String(100), 
        unique=True, 
        nullable=False
        )
    password : Mapped[str] = mapped_column(
        String(255), 
        nullable=False
        )
    created_at : Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        )
    updated_at : Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        )
    
