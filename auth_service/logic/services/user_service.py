from models.users import User
from logic.interfaces.iuser_respository import IUserRepository
from logic.interfaces.ibase_strategy import IBaseStrategy
from errorhub.exceptions import ConflictException
from errorhub.models import ErrorSeverity


class UserService(object):
    def __init__(self, user_repo: IUserRepository, base_strategy: IBaseStrategy):
        self.user_repository = user_repo
        self.base_strategy = base_strategy

    async def register_user(self, user: User) -> User:
        if await self.user_repository.get_user_by_id(str(user.id)) is not None:
            raise ConflictException(
                service="auth_service", message="User Id already exists", severity=ErrorSeverity.LOW
            )
        if await self.user_repository.get_user_by_email(user.email) is not None:
            raise ConflictException(service="auth_service", message="Email already exists", severity=ErrorSeverity.LOW)
        hashed_password = self.base_strategy.hash_password(user.password_hash)
        user.password_hash = hashed_password
        user_created = await self.user_repository.create_user(user)
        return user_created

    async def delete_user(self, user_id: str) -> dict:
        if await self.user_repository.get_user_by_id(user_id) is None:
            return {"error": "User not found"}

        await self.user_repository.delete_user(user_id)
        return {"message": "User deleted successfully"}

    async def update_user_by_id(self, user_id: str, user: User) -> dict | User:
        if await self.user_repository.get_user_by_id(user_id) is None:
            return {"error": "User not found"}

        await self.user_repository.update_user(user)
        return user

    async def get_user_info(self, user_id: str | None, user_email: str | None) -> dict | User:
        if not user_id and not user_email:
            return {"error": "User id or email is required"}
        if user_id:
            user = await self.user_repository.get_user_by_id(user_id)
        elif user_email:
            user = await self.user_repository.get_user_by_email(user_email)

        if user is None:
            return {"error": "User not found"}
        return user
