
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
        

    async def login_user(self,email: str,
    password: str,):
        # Fetch user and check whether user exist
        db_user = await self.user_repo.get_user_by_email(email)
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Compare password
        if not verify_password(password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate Access token
        jwt_helper = JWTHelper()
        payload={
            "sub": str(db_user.id),
            "email": db_user.email,
        }
        access_token = jwt_helper.create_access_token({
            "sub": str(db_user.id),
            "email": db_user.email,
        })

        refresh_token = jwt_helper.create_refresh_token({
            "sub": str(db_user.id),
        })

        # Return token
        return {"access_token":access_token, "refresh_token":refresh_token}
    
    async def refresh_access_token(self, refresh_token: str):
        jwt_helper = JWTHelper()

        # Verify refresh token
        payload = jwt_helper.decode_refresh_token(refresh_token)

        # Extract user id
        user_id = payload["sub"]

        # Check user still exists
        db_user = await self.user_repo.get_user_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Create new access token
        new_access_token = jwt_helper.create_access_token({
            "sub": str(db_user.id),
            "email": db_user.email,
        })

        return {
            "access_token": new_access_token
    }


        