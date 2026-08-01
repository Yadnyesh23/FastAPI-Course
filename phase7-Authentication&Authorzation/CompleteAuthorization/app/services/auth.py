
from app.schemas.request.auth import RegisterRequest, LoginRequest
from app.models.user import UserModel
from app.repository.user import UserRepository
from app.core.security import hash_password, verify_password
from fastapi import HTTPException

class AuthService:
    def __init__(self,user_repo:UserRepository):
        self.user_repo = user_repo

    async def register_user(self,user:RegisterRequest):
        db_user = await self.user_repo.get_user_by_email(user.email)

        if db_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = hash_password(user.password)

        new_user = UserModel(
            username=user.username,
            email=user.email,
            password=hashed_password,
        )

        await self.user_repo.create_user(new_user)
        
        return new_user
        

    async def login_user(self,user:LoginRequest):
        pass

        