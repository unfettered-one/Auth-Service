from auth_service.aws_proxy.dynamoDb.client_manager import DynamoDBClientManager
from auth_service.aws_proxy.dynamoDb.dynamo_operations import DynamoDBOperations
from botocore.client import BaseClient


def get_dynamodb_client(region_name: str) -> BaseClient:
    """
    Returns a singleton DynamoDB client per Lambda container.
    """
    return DynamoDBClientManager.get_client(region_name)


def get_dynamodb_operations(table_name: str, region_name: str) -> "DynamoDBOperations":
    """
    Factory function to create DynamoDBOperations instance.
    """
    return DynamoDBOperations(table_name, region_name)
