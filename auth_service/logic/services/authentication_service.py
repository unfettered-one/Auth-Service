"""
Authentication service is layer between Auth strategies like email/password, google..etc and Auth apis
"""

from interfaces.iauthentication_service import IAuthenticationService
from interfaces.iauth_strategy import IAuthStrategy
from models.users import User


class AuthenticationService(IAuthenticationService):
    def __init__(self, strategies: dict[str, IAuthStrategy]):
        """
        :param strategies: A dict of strategy_name -> strategy_instance
        :param token_service: A service for generating/verifying JWTs or sessions
        """
        self.strategies = strategies

    async def login(self, credentials: dict, strategy_name: str) -> dict:
        # Get the strategy
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            raise ValueError(f"Unsupported authentication strategy: {strategy_name}")

        # Authenticate user using the chosen strategy
        user = await strategy.authenticate(credentials)

        # Issue JWT (or session token)
        access_token = "access token"
        refresh_token = "refresh token"

        return {"user": user, "access_token": access_token, "refresh_token": refresh_token}

    async def logout(self, user_id: str, strategy_name: str) -> dict:
        """
        For JWT: often nothing to do except client-side token removal.
        For sessions: invalidate session.
        """
        # If using sessions, call session_service.invalidate(user_id)
        return {"message": f"User {user_id} logged out"}
