from app.core.jwt import create_access_token

class AuthService:

    def login_user(user):
        # Fetch user 
        # Verify password
        # Generate Token
        token = create_access_token(user)
        return {
            'email' : user.email,
            "access_token" : token
        }
        