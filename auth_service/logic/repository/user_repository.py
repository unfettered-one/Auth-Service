from logic.interfaces.iuser_respository import IUserRepository
from configuration import settings
from models.users import User
import json


class JsonUserRepository(IUserRepository):
    def __init__(self):
        self.file_path = settings.get_user_json_record_path()

        self.user_dict = json.load(open(self.file_path, encoding="utf-8"))

    async def create_user(self, user: User) -> User:
        self.user_dict[str(user.id)] = user.model_dump()
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.user_dict, f, indent=4, default=str)
        return user

    async def get_user_by_email(self, email: str):
        for user in self.user_dict.values():
            if user.get("email") == email:
                return User(**user)
        return None

    async def get_user_by_id(self, user_id: str):
        user_data = self.user_dict.get(user_id)
        if user_data:
            return User(**user_data)
        return None

    async def update_user(self, user: User):
        self.user_dict[user.id] = user.model_dump()
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.user_dict, f, indent=4, default=str)

    async def delete_user(self, user_id: str):
        self.user_dict.pop(user_id, None)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.user_dict, f, indent=4, default=str)
