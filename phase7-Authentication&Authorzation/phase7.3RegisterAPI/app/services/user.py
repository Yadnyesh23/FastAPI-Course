from app.schemas.request.user import RegisterUserRequestModel
from app.repository.user import UserRepository
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


class UserService:

    def validate_user_data(user):
        if user.name is None or user.name == "":
            return False, "Name is required"
        if user.email is None or user.email == "":
            return False, "Email is required"
        if user.password is None or user.password == "":
            return False, "Password is required"
        return True, "User data is valid"
    
    def regsiter_user(user_data : RegisterUserRequestModel):
        # 1. Get user data from request
        user = user_data.model_dump()

        # 2. Validate User data
        is_valid_user, msg = UserService.validate_user_data(user)

        if not is_valid_user:
            return {"message" : msg}, 400

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
        # 7. Return User Data + Access Token
        