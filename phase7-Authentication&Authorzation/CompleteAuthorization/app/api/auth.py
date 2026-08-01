from app.repository.user import UserRepository
from fastapi import APIRouter, Depends

from app.schemas.request.auth import RegisterRequest
from app.schemas.response.auth import RegisterResponse
from app.services.auth import AuthService
from app.database.db import get_db

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
    )



@router.post('/register',response_model=RegisterResponse,status_code=201)
async def register_user(
    user : RegisterRequest,
    db=Depends(get_db)
):
    repo = UserRepository(db)
    service = AuthService(repo)
    result = await service.register_user(user)
    user = {
        "username":result.username,
        "email":result.email,
        "password":result.password
    }
    return {
        "message":"User registered successfully",
        "user":user
    }