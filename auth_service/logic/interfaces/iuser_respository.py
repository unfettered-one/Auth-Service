"""
Interface/Abstract class for User Repository
"""

from abc import ABC, abstractmethod
from models.users import User


class IUserRepository(ABC):
    """
    User Interface / Abstract class for User Repository, use this every where rather than real repository
    """

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """
        abstract method to create user
        """

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """
        abstract method to get user by email
        """

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> User | None:
        """
        abstract method to get user by id
        """

    @abstractmethod
    async def update_user(self, user: User) -> User:
        """
        abstract method to update user
        """

    @abstractmethod
    async def delete_user(self, user_id: str) -> None:
        """
        abstract method to delete user
        """
