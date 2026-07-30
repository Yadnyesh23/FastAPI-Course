from sqlalchemy import select

from app.models.user import UserModel

class UserRepository():

    def get_user_by_email(self, email: str):
        stmt = select(UserModel).where(UserModel.email == email)

        result = execute(stmt)

        return result.scalar_one_or_none()