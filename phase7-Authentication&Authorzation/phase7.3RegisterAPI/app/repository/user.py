from sqlalchemy import select, insert, update, delete

from app.models.user import UserModel
from app.database import SessionLocal as session

class UserRepository:

    def get_user_by_id(id):
        stmt = select(UserModel).where(UserModel.id == id)
        result = session.execute(stmt)
        return result.scalar_one_or_none()

    def get_user_by_email(email):
        stmt = select(UserModel).where(UserModel.email == email)
        result =- session.execute(stmt)
        return result.scalar_one_or_none()

    def create_user(user):
        try:
            stmt = insert(UserModel).values(**user.model_dump())
            session.execute(stmt)
            return True
        except Exception as e:
            session.rollback()
            return False

    def update_user(id, user):
        try:
            stmt = update(UserModel).where(UserModel.id == id).values(**user.model_dump())
            session.execute(stmt)
            return True
        except Exception as e:
            session.rollback()
            return False

    def delete_user(id):
        try:
            stmt = delete(UserModel).where(UserModel.id == id)
            session.execute(stmt)
            return True
        except Exception as e:
            session.rollback()
            return False