from datetime import UTC, datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException
from app.core.config import settings


class JWTHelper:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.access_expiry_time = settings.JWT_ACCESS_TOKEN_EXPIRY_MINUTES
        self.refresh_expiry_time = settings.JWT_REFRESH_TOKEN_EXPIRY_DAYS


    def create_access_token(self,payload:dict)->str:
        """Encode token"""
        payload = payload.copy()
        payload["type"] = "access"
        payload["exp"] = datetime.now(UTC) + timedelta(minutes=self.access_expiry_time)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self,payload:dict)->str:
        """Encode token"""
        payload = payload.copy()
        payload["type"] = "refresh"
        payload["exp"] = datetime.now(UTC) + timedelta(days=self.refresh_expiry_time)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self,token:str)->dict:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token has expired"
            )

        except InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid access token"
            )

    def decode_access_token(self, token):
        payload = self.decode(token)

        if payload.get("type") != "access":
            raise HTTPException("Invalid access token")

        return payload
    
    def decode_refresh_token(self, token):
        payload = self.decode(token)

        if payload.get("type") != "refresh":
            raise HTTPException("Invalid refresh token")

        return payload