from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings


def create_access_token(data: dict[str, Any]) -> str:
    """
    Create and sign a JWT access token.

    Args:
        data: Claims to include in the payload.
              Example:
              {
                  "sub": "<user_id>",
                  "email": "abc@gmail.com",
                  "role": "user"
              }

    Returns:
        Encoded JWT token.
    """

    # Create a copy so the original dictionary isn't modified
    payload = data.copy()

    # Current UTC time
    now = datetime.now(timezone.utc)

    # Token expiration time
    expire = now + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Standard JWT Claims
    payload.update(
        {
            "iat": now,
            "exp": expire,
        }
    )

    # Generate signed JWT
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return token


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Verify and decode a JWT.

    Args:
        token: JWT string

    Returns:
        Decoded payload

    Raises:
        ExpiredSignatureError:
            If token has expired.

        InvalidTokenError:
            If token is invalid or signature verification fails.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload

    except ExpiredSignatureError:
        raise ValueError("Token has expired")

    except InvalidTokenError:
        raise ValueError("Invalid token")