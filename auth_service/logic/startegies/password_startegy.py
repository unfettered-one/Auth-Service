"""
Basic email/password authentication strategy
"""

from auth_service.logic.interfaces.iauth_strategy import IAuthStrategy
from auth_service.logic.interfaces.iuser_respository import IUserRepository
from auth_service.utils.password import verify_password

from errorhub.exceptions import NotFoundException, UnauthorizedException
from errorhub.models import ErrorSeverity

from auth_service.configuration import settings
from auth_service.models.users import User


class EmailPasswordStrategy(IAuthStrategy):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def authenticate(self, credentials: dict) -> User | None:
        email = credentials["email"]
        password = credentials["password"]

        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise NotFoundException(
                service="Auth Service",
                message="User not found",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
                context={
                    "detail": " No registered user found for authentication.",
                    "suggestion": "Register first please... or enter correct email",
                },
            )
        if user and verify_password(password, user.password_hash):
            return user
        raise UnauthorizedException(
            service="Auth Service",
            message="Invalid credentials",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "Authentication failed",
                "suggestion": "Please enter correct password",
            },
        )
