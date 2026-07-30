from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.schemas.request.auth import LoginRequestModel
from app.schemas.response.auth import (
    LoginResponseModel,
    UserInfo,
)
from app.repository.user import UserRepository


password_hash = PasswordHash.recommended()


class AuthService:

    def __init__(self):
        # self.db = db
        self.user_repository = UserRepository()

    def login(self, request: LoginRequestModel):

        # 1. Find user
        user = self.user_repository.get_user_by_email(
            request.email
        )

        # 2. User not found
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # 3. Verify password
        if not password_hash.verify(
            request.password,
            user.password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # 4. Generate JWT
        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
            }
        )

        # 5. Return response
        return LoginResponseModel(
            access_token=access_token,
            user=UserInfo(
                id=user.id,
                name=user.name,
                email=user.email,
            ),
        )