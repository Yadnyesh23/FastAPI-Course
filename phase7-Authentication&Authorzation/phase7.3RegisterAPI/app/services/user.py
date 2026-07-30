from app.schemas.request.user import RegisterUserRequestModel
from app.schemas.response.user import RegisterUserResponseModel
from app.repository.user import UserRepository
from pwdlib import PasswordHash
from app.core.jwt import create_access_token

password_hash = PasswordHash.recommended()


class UserService:

 
    
    def regsiter_user(user_data):
        # 1. Get user data from request
        user = user_data.model_dump()

        # 3. check if user already exist or not(by email)
        is_user_exist = UserRepository.get_user_by_email(user["email"])

        if is_user_exist:
            return {"message" : "User already exist"}, 400

        # 4. Hash the password
        hashed_password = password_hash.hash(user["password"])
        user["password"] = hashed_password
        
        # 5. Call Repository layer to create user
        result = UserRepository.create_user(user)
        
        if not result:
            return {"message" : "User not created"}, 500
        # 6. Generate Access Token
        access_token = create_access_token({"email" : user["email"]})

        # 7. Return User Data + Access Token
        return RegisterUserResponseModel(
            username = user["username"],
            email = user["email"],
            access_token = access_token,
            token_type = "bearer"
        )