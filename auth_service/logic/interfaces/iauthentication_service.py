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
    async def login(self, email: str, password: str) -> dict | User:
        """
        Login user with email and password
        """

    @abstractmethod
    async def logout(self, user_id: str) -> dict:
        """
        Logout user with user_id
        """

    @abstractmethod
    async def verify_token(self, token: str) -> dict | User:
        """
        Verify user token
        """

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> dict:
        """
        Refresh user token
        """
