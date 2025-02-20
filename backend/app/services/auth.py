from datetime import datetime, timedelta
import jwt
from ..core.config import settings

class AuthService:
    @staticmethod
    async def login(username: str, password: str):
        """
        Simple login that accepts any credentials for testing
        """
        # For testing, create a simple user_id based on username
        user_id = "test_" + username.lower()
        
        # Create a simple JWT token
        token = jwt.encode(
            {
                "user_id": user_id,
                "username": username,
                "exp": datetime.utcnow() + timedelta(days=1)
            },
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        
        return {
            "user_id": user_id,
            "username": username,
            "access_token": token
        } 