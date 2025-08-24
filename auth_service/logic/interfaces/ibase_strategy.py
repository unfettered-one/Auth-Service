from abc import ABC, abstractmethod


class IBaseStrategy(ABC):
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash the password and return the hash."""
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify if the plain password matches the hash."""
        pass
