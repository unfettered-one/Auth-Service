"""
Connection between user apis and user repository.
"""

from auth_service.models.users import User
from auth_service.logic.interfaces.iuser_respository import IUserRepository
from auth_service.utils.password import hash_password

from errorhub.exceptions import ConflictException, NotFoundException, BadRequestException
from errorhub.models import ErrorSeverity

from auth_service.configuration import settings


class UserService:
    """
    User Service for managing user-related operations.
    This layer connects the user repository and api layer together.
    """

    def __init__(self, user_repo: IUserRepository):
        self.user_repository = user_repo

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
        hashed_password = await hash_password(user.password_hash)
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

    async def update_user_by_id(self, user_id: str, user: User) -> User:
        """
        Update user information by user_id.
        """
        old_user = await self.user_repository.get_user_by_id(user_id)
        if old_user is None:
            raise NotFoundException(
                service="auth_service",
                message="User not found",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
                context={"The user you are trying to update is not found": user_id},
            )
        if user.email != old_user.email and len(user.email) > 0:
            old_user.email = user.email
        if user.name != old_user.name:
            old_user.name = user.name
        if user.apps != old_user.apps and len(user.apps) > 0:
            old_user.apps = user.apps
        if user.password_hash != old_user.password_hash and len(user.password_hash) > 0:
            hashed_password = await hash_password(user.password_hash)
            old_user.password_hash = hashed_password
        if user.updated_at:
            old_user.updated_at = user.updated_at
        new_user = await self.user_repository.update_user(old_user)
        return new_user

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
