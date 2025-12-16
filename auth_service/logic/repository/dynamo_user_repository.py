"""
Connection between DynamoDB users table and user service layer
"""

from typing import Type

from auth_service.logic.interfaces.iuser_respository import IUserRepository
from auth_service.models.users import User
from auth_service.aws_proxy.utils import get_dynamodb_operations

from auth_service.configuration import settings
from errorhub.exceptions import NotFoundException, InternalServerErrorException
from errorhub.models import ErrorSeverity

from errorhub.models import BaseModel


class DynamoDBUserRepository(IUserRepository):
    """
    Real CRUD operations for user data happens here using DynamoDB.
    This is the ONLY repository you should use in production.
    """

    def __init__(self):
        self._region = settings.get_aws_region()
        self._table_name = settings.get_user_dynamo_table_name()
        if self._table_name is None:
            raise NotFoundException(service="AuthService", message="DynamoDB table name for users is not configured.")
        self.users_table = get_dynamodb_operations(self._table_name, self._region)

    async def create_user(self, user: User) -> User:
        """
        create user in DynamoDB
        """
        item = user.model_dump()
        if "name" in item:
            item["user_name"] = item.pop("name")
        item["pk"] = f"USER#{user.id}"

        self.users_table.create_item(item)
        return user

    async def get_user_by_email(self, email: str) -> User | None:
        """
        find user by email using a GSI (email-index)
        """
        # Query the GSI to get the pk (user_id)
        response = self.users_table.client.query(
            TableName=self.users_table.table_name,
            IndexName="email-index",
            KeyConditionExpression="email = :email",
            ExpressionAttributeValues={":email": {"S": email}},
            Limit=1,
        )

        items = response.get("Items", [])
        if not items:
            return None

        # Extract the pk from the GSI item
        pk = items[0]["pk"]["S"]  # Assuming pk is projected in the GSI

        # Now get the full item from the main table
        full_item = self.users_table.get_item({"pk": pk})

        if full_item:
            return User(**await self._filter_for_user_model(User, full_item))
        return None

    async def _filter_for_user_model(self, model: Type[BaseModel], data: dict) -> dict:
        """
        filter data for user model
        """
        if "user_name" in data:
            data["name"] = data.pop("user_name")
        allowed_fields = set(model.model_fields.keys())
        return {k: v for k, v in data.items() if k in allowed_fields}

    async def get_user_by_id(self, user_id: str) -> User | None:
        """
        find user by id
        """
        item = self.users_table.get_item({"pk": f"USER#{user_id}"})

        if item:
            return User(**await self._filter_for_user_model(User, item))
        return None

    async def update_user(self, user: User) -> User:
        """
        update user in DynamoDB
        """
        key = {"pk": f"USER#{user.id}"}

        update_expression = """
            SET email = :email,
                user_name = :name,
                apps = :apps,
                updated_at = :updated_at,
                password_hash = :password_hash
        """

        expression_values = {
            ":email": user.email,
            ":name": user.name,
            ":password_hash": user.password_hash,
            ":apps": user.apps,
            ":updated_at": user.updated_at,
        }

        self.users_table.update_item(key=key, update_expression=update_expression, expression_values=expression_values)
        new_user = await self.get_user_by_id(user.id)
        if new_user is None:
            raise InternalServerErrorException(
                service="auth_service",
                message="Failed to update user",
                severity=ErrorSeverity.HIGH,
                environment=settings.get_environment(),
                context={"detail": f"User with id {user.id} not found after update."},
            )
        return new_user

    async def delete_user(self, user_id: str):
        """
        delete user from DynamoDB
        """
        self.users_table.delete_item({"pk": f"USER#{user_id}"})
