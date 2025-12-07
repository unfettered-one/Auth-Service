"""
Connection between DynamoDB users table and user service layer
"""

from logic.interfaces.iuser_respository import IUserRepository
from models.users import User
from auth_service.aws_proxy.utils import get_dynamodb_operations


class DynamoDBUserRepository(IUserRepository):
    """
    Real CRUD operations for user data happens here using DynamoDB.
    This is the ONLY repository you should use in production.
    """

    def __init__(self):
        self.users_table = get_dynamodb_operations("users", "us-east-1")

    async def create_user(self, user: User) -> User:
        """
        create user in DynamoDB
        """
        item = user.model_dump()
        item["pk"] = f"USER#{user.id}"
        item["sk"] = "PROFILE"

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
        full_item = self.users_table.get_item({"pk": pk, "sk": "PROFILE"})

        if full_item:
            return User(**full_item)
        return None

    async def get_user_by_id(self, user_id: str):
        """
        find user by id
        """
        item = self.users_table.get_item({"pk": f"USER#{user_id}", "sk": "PROFILE"})

        if item:
            return User(**item)
        return None

    async def update_user(self, user: User):
        """
        update user in DynamoDB
        """
        key = {"pk": f"USER#{user.id}", "sk": "PROFILE"}

        update_expression = "SET email = :email"

        expression_values = {":email": user.email}

        self.users_table.update_item(key=key, update_expression=update_expression, expression_values=expression_values)

    async def delete_user(self, user_id: str):
        """
        delete user from DynamoDB
        """
        self.users_table.delete_item({"pk": f"USER#{user_id}", "sk": "PROFILE"})
