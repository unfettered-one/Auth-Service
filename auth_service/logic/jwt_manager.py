from models.users import User


class JWTManager:
    async def verify_token(self, token: str):
        """
        Verify user token
        """

    async def refresh_token(self, refresh_token: str):
        """
        Refresh user token
        """
