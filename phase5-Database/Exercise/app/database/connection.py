from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://postgres:123456@localhost:5432/fastapi_learning"

engine = create_engine(DATABASE_URL)