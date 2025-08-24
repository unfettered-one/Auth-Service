from factory import Factory
from models.users import User


class UserService(object):
    def __init__(self):
        self.user_repository = Factory.get_user_repository()
        self.base_strategy = Factory.get_base_strategy()

    async def register_user(self, user: User) -> dict | User:
        if await self.user_repository.get_user_by_id(str(user.id)) is not None:
            return {"error": "User Id already exists"}
        if await self.user_repository.get_user_by_email(user.email) is not None:
            return {"error": "Email already exists"}
        hashed_password = self.base_strategy.hash_password(user.password_hash)
        user.password_hash = hashed_password
        await self.user_repository.create_user(user)
        return user

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
