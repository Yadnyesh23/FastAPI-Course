from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.user import router as user_router
from app.api.upload import router as upload_router
from app.core.middlewares import register_middlewares

app = FastAPI()

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(upload_router)
register_middlewares(app)
