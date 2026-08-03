from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user
from app.models.user import UserModel

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get('/me')
async def get_me(user : UserModel = Depends(get_current_user)):
    return user
