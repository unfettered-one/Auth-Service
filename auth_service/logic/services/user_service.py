"""
Connection between user apis and user repository.
"""

from models.users import User
from logic.interfaces.iuser_respository import IUserRepository
from logic.interfaces.ibase_strategy import IBaseStrategy
from errorhub.exceptions import ConflictException, NotFoundException, BadRequestException
from errorhub.models import ErrorSeverity
from configuration import settings


class UserService:
    """
    User Service for managing user-related operations.
    This layer connects the user repository and api layer together.
    """

    def __init__(self, user_repo: IUserRepository, base_strategy: IBaseStrategy):
        self.user_repository = user_repo
        self.base_strategy = base_strategy

    async def register_user(self, user: User) -> User:
        """
        Create a new user.
        """
        if await self.user_repository.get_user_by_id(str(user.id)) is not None:
            raise ConflictException(
                service="auth_service",
                message="User Id already exists",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
            )
        if await self.user_repository.get_user_by_email(user.email) is not None:
            raise ConflictException(
                service="auth_service",
                message="Email already exists",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
            )
        hashed_password = self.base_strategy.hash_password(user.password_hash)
        user.password_hash = hashed_password
        user_created = await self.user_repository.create_user(user)
        return user_created

    async def delete_user(self, user_id: str) -> None:
        """
        Delete a user by user_id.
        """
        if await self.user_repository.get_user_by_id(user_id) is None:
            raise NotFoundException(
                service="auth_service",
                message="User not found",
                severity=ErrorSeverity.LOW,
                context={"The user you are trying to delete is not found": user_id},
                environment=settings.get_environment(),
            )

        await self.user_repository.delete_user(user_id)

    async def update_user_by_id(self, user_id: str, user: User) -> dict | User:
        """
        Update user information by user_id.
        """
        if await self.user_repository.get_user_by_id(user_id) is None:
            return {"error": "User not found"}

        await self.user_repository.update_user(user)
        return user

    async def get_user_info(self, user_id: str | None, user_email: str | None) -> User:
        """
        Get user information by user_id or user_email.
        """
        if not user_id and not user_email:
            raise BadRequestException(
                service="auth_service",
                message="user_id or user_email must be provided",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
            )

        if user_id:
            user = await self.user_repository.get_user_by_id(user_id)
        elif user_email:
            user = await self.user_repository.get_user_by_email(user_email)
        else:
            user = None
        if user is None:
            raise NotFoundException(
                service="auth_service",
                message="User not found",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
            )
        return user
