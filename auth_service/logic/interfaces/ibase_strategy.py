"""
Interface/ Abstract class for Password Hashing Strategy
"""

from abc import ABC, abstractmethod


class IBaseStrategy(ABC):
    """
    Base interface for password hashing strategies, use this to import everywhere rather than real strategy
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash the password and return the hash."""

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify if the plain password matches the hash."""
