"""
Factory module that is used everywhere to create instances of services
"""

from logic.interfaces.iuser_respository import IUserRepository
from logic.repository.user_repository import JsonUserRepository
from logic.interfaces.ibase_strategy import IBaseStrategy
from logic.startegies.password_startegy import BcryptPasswordStrategy

from logic.services.user_service import UserService


class Factory:
    """
    Factory class for creating service instances
    """

    @staticmethod
    def get_user_repository() -> IUserRepository:
        """
        Returns an instance of the user repository
        """
        return JsonUserRepository()

    @staticmethod
    def get_user_service() -> UserService:
        """
        Returns an instance of the user service
        """
        user_repo = JsonUserRepository()
        base_strategy = BcryptPasswordStrategy()
        return UserService(user_repo, base_strategy)

    @staticmethod
    def get_base_strategy() -> IBaseStrategy:
        """
        Returns an instance of the base strategy
        """
        return BcryptPasswordStrategy()


factory = Factory()
