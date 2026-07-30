from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/Phase7.5loginDB"
engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase):
    pass