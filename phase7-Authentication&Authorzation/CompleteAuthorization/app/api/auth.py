from app.core.jwt import JWTHelper
from fastapi import APIRouter, Depends

from app.database.db import get_db
from app.repository.user import UserRepository
from app.schemas.request.auth import LoginRequest, RegisterRequest, RefreshTokenRequest
from app.schemas.response.auth import LoginResponse, RegisterResponse, RefreshTokenResponse
from app.services.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm

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
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db)
):
    repo = UserRepository(db)
    service = AuthService(repo)
    result = await service.login_user(email=form_data.username,
    password=form_data.password,)
    return {
        "message":"User logged in successfully",
        "access_token":result["access_token"]
    }


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=200
)
async def refresh_access_token(
    request: RefreshTokenRequest,
    db=Depends(get_db),
):
    repo = UserRepository(db)
    service = AuthService(repo)

    result = await service.refresh_access_token(request.refresh_token)

    return {
        "message": "Access token refreshed successfully",
        "access_token": result["access_token"],
        "refresh_token": result["refresh_token"],
        "token_type": "bearer"
    }

