from auth_service.logic.services.user_service import UserService
from logic.interfaces.iuser_respository import IUserRepository
from logic.repository.user_repository import JsonUserRepository
from logic.interfaces.ibase_strategy import IBaseStrategy
from logic.startegies.password_startegy import PasswordStrategy


class Factory(object):
    @staticmethod
    def get_user_repository() -> IUserRepository:
        return JsonUserRepository()

    @staticmethod
    def get_user_service() -> UserService:
        return UserService()

    @staticmethod
    def get_base_strategy() -> IBaseStrategy:
        return PasswordStrategy()
