import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "aVxnSBMypp5tTDZKZpSctq3ICpWF4qJH65ZsYF8h5lw="
ALGORITHM = "HS256"


def create_access_token(data : dict):
    payload = data.copy()

    now = datetime.now(timezone.utc)

    expires = now + timedelta(minutes=60)
    payload["exp"] = expires
    payload["iat"] = now

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token : str) -> dict :
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        return "Token Expired"
    except jwt.InvalidTokenError:
        return "Invalid Token"
    except Exception as e:
        return str(e)