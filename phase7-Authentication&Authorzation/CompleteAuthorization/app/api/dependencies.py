from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.core.security import oauth2_scheme
from app.core.jwt import JWTHelper
from app.repository.user import UserRepository

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    jwt_helper = JWTHelper()
    payload = jwt_helper.decode(token)

    user_id = payload["sub"]

    repo = UserRepository(db)
    user = await repo.get_user_by_id(user_id)   

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user