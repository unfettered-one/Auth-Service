"""
Authentication service is layer between Auth strategies like email/password, google..etc and Auth apis
"""

from logic.interfaces.iauthentication_service import IAuthenticationService
from logic.interfaces.iauth_strategy import IAuthStrategy
from logic.interfaces.itoken_service import ITokenService

from configuration import settings

from models.users import User

from errorhub.exceptions import UnauthorizedException, NotFoundException
from errorhub.models import ErrorSeverity


class AuthenticationService(IAuthenticationService):
    def __init__(self, strategies: dict[str, IAuthStrategy], token_service: ITokenService) -> None:
        """
        :param strategies: A dict of strategy_name -> strategy_instance
        :param token_service: A service for generating/verifying JWTs or sessions
        """
        self.strategies = strategies
        self.token_service = token_service

    async def login(self, credentials: dict, strategy_name: str) -> dict:
        """
        Authenticate using the given strategy and generate tokens.
        """
        # Pick auth strategy
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            raise NotFoundException(
                service="Auth Service",
                message="Authentication strategy not found",
                severity=ErrorSeverity.MEDIUM,
                environment=settings.get_environment(),
                context={
                    "detail": f"Strategy '{strategy_name}' is not supported.",
                    "suggestion": "Please use a valid authentication strategy",
                },
            )

        # Authenticate user
        user: User | None = await strategy.authenticate(credentials)
        if not user:
            raise UnauthorizedException(
                service="Auth Service",
                message="Authentication failed",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
                context={
                    "detail": "Authentication failed",
                    "suggestion": "Please check your credentials and try again",
                },
            )
        # Generate real JWTs
        access_token = await self.token_service.generate_access_token(user)
        refresh_token = await self.token_service.generate_refresh_token(user)

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def logout(self, refresh_token: str, strategy_name: str) -> dict:
        """
        Logout by revoking the refresh token.
        """
        # For JWT-based auth, we only revoke refresh tokens.
        await self.token_service.revoke_refresh_token(refresh_token)

        return {"message": "User logged out successfully"}
