"""
Abstract/Interface for Authentication Service
"""

from abc import ABC, abstractmethod


class IAuthenticationService(ABC):
    """
    Interface for Authentication Service, use this everywhere rather than real service
    """

    @abstractmethod
    async def login(self, credentials: dict, strategy_name: str) -> dict:
        """
        Login with different strategies, eg (email and password),google, microsoft
        """

    @abstractmethod
    async def logout(self, refresh_token: str) -> dict:
        """
        Logout user with token
        """
