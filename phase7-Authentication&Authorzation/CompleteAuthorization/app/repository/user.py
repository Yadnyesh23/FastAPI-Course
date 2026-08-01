from typing import Optional
from app.models.user import UserModel

import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select

class UserRepository:
    def __init__(self, session:Session):
        self.session = session

    async def get_user_by_id(
        self,
        id:uuid.UUID
    ) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.id == id)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def get_user_by_email(
        self,
        email:str
    ) -> Optional[UserModel]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(
        self,
        user:UserModel
    ):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    async def update_user(
        self,
        id: uuid.UUID,
        updated_user: UserModel
    ):
        db_user = await self.get_user_by_id(id)

        if not db_user:
            return None

        db_user.username = updated_user.username
        db_user.email = updated_user.email
        db_user.password = updated_user.password

        self.session.commit()
        self.session.refresh(db_user)

        return db_user
        
        


    async def delete_user(self,id:uuid.UUID):
        user = await self.get_user_by_id(id)
        if not user:
            return None
        self.session.delete(user)
        self.session.commit()
        