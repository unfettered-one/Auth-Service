from abc import ABC, abstractmethod
from models.users import User


class IAuthenticationService(ABC):
    @abstractmethod
    async def login(self, email: str, password: str) -> dict | User:
        pass

    @abstractmethod
    async def logout(self, user_id: str) -> dict:
        pass

    @abstractmethod
    async def verify_token(self, token: str) -> dict | User:
        pass

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> dict:
        pass
