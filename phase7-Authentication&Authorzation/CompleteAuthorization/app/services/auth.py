
from fastapi import HTTPException

from app.core.jwt import JWTHelper
from app.core.security import hash_password, verify_password
from app.models.user import UserModel
from app.repository.user import UserRepository
from app.schemas.request.auth import LoginRequest, RegisterRequest


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
        # Fetch user and check whether user exist
        db_user = await self.user_repo.get_user_by_email(user.email)
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Compare password
        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate Access token
        jwt_helper = JWTHelper()
        payload={
            "email": db_user.email,
            "user_id": str(db_user.id)
        }
        jwt_token = jwt_helper.encode(payload)

        # Return token
        return {"access_token":jwt_token}


        