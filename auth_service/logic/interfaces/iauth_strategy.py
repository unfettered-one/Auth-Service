from abc import ABC, abstractmethod


class IAuthStrategy(ABC):
    @abstractmethod
    async def authenticate(self, credentials: dict):
        pass
