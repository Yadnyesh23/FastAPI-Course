from fastapi import APIRouter

from app.schemas.request.user import RegisterUserRequestModel
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register")
def register_user(user : RegisterUserRequestModel):
    result = UserService.register_user(user)
    return result
