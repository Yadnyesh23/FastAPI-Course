from datetime import UTC, datetime, timedelta

import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings


class JWTHelper:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
        self.expiry_time = settings.JWT_EXPIRY_TIME


    def encode(self,payload:dict)->str:
        """Encode token"""
        payload = payload.copy()
        payload["exp"] = datetime.now(UTC) + timedelta(minutes=self.expiry_time)
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self,token:str)->dict:
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )

        except ExpiredSignatureError:
            raise Exception("Token has expired")

        except InvalidTokenError:
            raise Exception("Invalid token")