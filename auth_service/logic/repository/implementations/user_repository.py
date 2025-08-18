from logic.repository.interfaces.iuser_respository import IUserRepository


class JsonUserRepository(IUserRepository):

    async def create_user(self, user):
        pass

    async def get_user_by_email(self, email: str):
        pass

    async def get_user_by_id(self, user_id: str):
        pass

    async def update_user(self, user):
        pass

    async def delete_user(self, user_id: str):
        pass
