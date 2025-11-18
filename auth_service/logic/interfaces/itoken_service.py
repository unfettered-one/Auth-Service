"""
Abstract interface for token services.
"""

from abc import ABC, abstractmethod
from models.users import User


class ITokenService(ABC):
    """
    Interface for Token Service, use this everywhere rather than real service
    """

    @abstractmethod
    async def generate_access_token(self, user: User) -> str:
        """
        abstract method to generate access token
        """
        pass

    @abstractmethod
    async def generate_refresh_token(self, user: User) -> str:
        """
        abstract method to generate refresh token
        """
        pass

    @abstractmethod
    async def verify_access_token(self, token: str) -> dict | None:
        """
        abstract method to verify access token
        """
        pass

    @abstractmethod
    async def verify_refresh_token(self, token: str) -> dict | None:
        """
        abstract method to verify refresh token
        """
        pass

    @abstractmethod
    async def revoke_refresh_token(self, token: str) -> None:
        """
        abstract method to revoke refresh token
        """
        pass

    @abstractmethod
    async def rotate_refresh_token(self, old_token: str) -> str:
        """
        abstract method to rotate refresh token
        """
        pass
