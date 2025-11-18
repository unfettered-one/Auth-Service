"""
Abstract/Interface for Authentication Service
"""

from abc import ABC, abstractmethod
from models.users import User


class IAuthenticationService(ABC):
    """
    Interface for Authentication Service, use this everywhere rather than real service
    """

    @abstractmethod
    async def login(self, credentials: dict, strategy_name: str) -> dict | User:
        """
        Login with different strategies, eg (email and password),google, microsoft
        """

    @abstractmethod
    async def logout(self, user_id: str, strategy_name: str) -> dict:
        """
        Logout user with user_id
        """
