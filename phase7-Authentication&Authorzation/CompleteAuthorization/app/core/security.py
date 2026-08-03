from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer


password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """hash password"""
    return password_hasher.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """verify password"""
    return password_hasher.verify(plain_password, hashed_password)



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)