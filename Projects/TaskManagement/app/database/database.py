from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings

# Create a engine(This is used tp create a connection with db)
engine = create_engine(settings.database_url)

# Create a session(This is used to create a session for each route)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
    )

# Use the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class Base(DeclarativeBase):
    pass