from logic.repository.interfaces.iuser_respository import IUserRepository
from logic.repository.implementations.user_repository import JsonUserRepository


class Factory(object):
    @staticmethod
    def get_user_repository() -> IUserRepository:
        return JsonUserRepository()
