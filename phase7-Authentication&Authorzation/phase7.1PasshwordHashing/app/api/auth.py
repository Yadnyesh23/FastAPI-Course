from fastapi import APIRouter

from app.service.auth import AuthService

router = APIRouter()

@router.post('/api/v1/register')
def register(name : str, email : str, password : str):

    user = AuthService.register_user(name, email, password)
    return {
        "message" : "User Registered Successfully",
        "data" : user
    }
    