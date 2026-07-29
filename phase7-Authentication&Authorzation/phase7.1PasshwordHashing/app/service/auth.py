from  app.core.security import hash_password, verify_password


class AuthService:

    def register_user(name, email, password):
        hashed_password = hash_password(password)
        return {
            "name" : name,
            "email" : email,
            "hashed_password" : hashed_password
        }

    def login_user(email, password):
        # check is user exists for the given email
        # check password is correct
        pass