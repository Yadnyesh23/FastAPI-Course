from fastapi import APIRouter, Depends

from app.database.db import get_db
from app.repository.user import UserRepository
from app.schemas.request.auth import LoginRequest, RegisterRequest
from app.schemas.response.auth import LoginResponse, RegisterResponse
from app.services.auth import AuthService

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


@router.post('/login', response_model=LoginResponse, status_code=200)
async def login_user(
    user : LoginRequest,
    db=Depends(get_db)
):
    repo = UserRepository(db)
    service = AuthService(repo)
    result = await service.login_user(user)
    return {
        "message":"User logged in successfully",
        "access_token":result["access_token"]
    }