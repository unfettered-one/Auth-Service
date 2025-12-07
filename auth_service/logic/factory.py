"""
Factory module that is used everywhere to create instances of services
"""

from logic.repository.json_user_repository import JsonUserRepository
from logic.services.user_service import UserService
from logic.services.authentication_service import AuthenticationService

from logic.interfaces.iauth_strategy import IAuthStrategy
from logic.interfaces.iauthentication_service import IAuthenticationService
from logic.services.jwt_token_service import JWTTokenService

from logic.startegies.password_startegy import EmailPasswordStrategy
from logic.startegies.google_strategy import GoogleAuthStrategy
from configuration import settings


class Factory:
    """
    Factory class for creating service instances
    """

    @staticmethod
    def get_user_service() -> UserService:
        """
        Returns an instance of the user service
        """
        user_repo = JsonUserRepository()
        return UserService(user_repo)

    @staticmethod
    def get_authentication_service() -> IAuthenticationService:
        """
        Returns an instance of the authentication service
        """

        # Build user repository
        user_repo = JsonUserRepository()

        # Build strategies
        strategies: dict[str, IAuthStrategy] = {
            "email_password": EmailPasswordStrategy(user_repository=user_repo),
            "google": GoogleAuthStrategy(user_repository=user_repo),
        }

        # Build token service
        token_service = JWTTokenService(
            secret_key=settings.get_jwt_secret() or "default_secret_key",
            access_token_expiry_minutes=15,
            refresh_token_expiry_days=7,
        )

        # Create fully-wired authentication service
        return AuthenticationService(
            strategies=strategies,
            token_service=token_service,
            user_repository=user_repo,
        )


factory = Factory()
