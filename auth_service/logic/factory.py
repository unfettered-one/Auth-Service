"""
Factory module that is used everywhere to create instances of services
"""

from logic.repository.user_repository import JsonUserRepository
from logic.services.user_service import UserService


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


factory = Factory()
