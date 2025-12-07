
from auth_service.aws_proxy.dynamoDb.dynamo_operations import DynamoDBOperations





def get_dynamodb_operations(table_name: str, region_name: str) -> "DynamoDBOperations":
    """
    Factory function to create DynamoDBOperations instance.
    """
    return DynamoDBOperations(table_name, region_name)
