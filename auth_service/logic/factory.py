"""
Factory module that is used everywhere to create instances of services
"""

from logic.repository.user_repository import JsonUserRepository
from logic.services.user_service import UserService

from logic.services.authentication_service import AuthenticationService

from interfaces.iauth_strategy import IAuthStrategy
from logic.startegies.password_startegy import EmailPasswordStrategy


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
    def get_authentication_service() -> AuthenticationService:
        """
        Returns an instance of the authentication service
        """
        # Build repository and concrete strategies to inject into the authentication service
        user_repo = JsonUserRepository()
        strategies: dict[str, IAuthStrategy] = {
            "email_password": EmailPasswordStrategy(user_repo),
        }

        return AuthenticationService(strategies)


factory = Factory()
