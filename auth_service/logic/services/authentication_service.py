"""
Authentication service is layer between Auth strategies like email/password, google..etc and Auth apis
"""

from logic.interfaces.iauthentication_service import IAuthenticationService
from logic.interfaces.iauth_strategy import IAuthStrategy
from logic.interfaces.itoken_service import ITokenService
from logic.interfaces.iuser_respository import IUserRepository

from configuration import settings

from models.users import User

from errorhub.exceptions import UnauthorizedException, NotFoundException
from errorhub.models import ErrorSeverity


class AuthenticationService(IAuthenticationService):
    def __init__(
        self, strategies: dict[str, IAuthStrategy], token_service: ITokenService, user_repository: IUserRepository
    ) -> None:
        """
        :param strategies: A dict of strategy_name -> strategy_instance
        :param token_service: A service for generating/verifying JWTs or sessions
        """
        self.strategies = strategies
        self.token_service = token_service
        self.user_repository = user_repository

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

    async def logout(self, refresh_token: str) -> dict:
        """
        Logout by revoking the refresh token.
        """
        # For JWT-based auth, we only revoke refresh tokens.
        await self.token_service.revoke_refresh_token(refresh_token)

        return {"message": "User logged out successfully"}

    async def refresh(self, refresh_token: str) -> dict:
        """
        Refresh access and refresh tokens using the provided refresh token.
        """
        # Verify refresh token
        payload = await self.token_service.verify_refresh_token(refresh_token)
        if not payload:
            raise UnauthorizedException(
                service="Auth Service",
                message="Invalid or expired refresh token",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
                context={
                    "detail": "The provided refresh token is invalid or has expired.",
                    "suggestion": "Please login again.",
                },
            )
        user_id = payload.get("sub", "")
        # Extract user info from payload
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise NotFoundException(
                service="Auth Service",
                message="User not found",
                severity=ErrorSeverity.MEDIUM,
                environment=settings.get_environment(),
                context={"detail": "User linked to refresh token does not exist"},
            )
        # Generate new tokens
        new_access_token = await self.token_service.generate_access_token(user)
        new_refresh_token = await self.token_service.rotate_refresh_token(refresh_token)
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
        }
