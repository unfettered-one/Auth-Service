from typing import Dict, Any, Optional
from aws_proxy.dynamoDb.util import get_dynamodb_client


class DynamoDBOperations:
    """
    Generic DynamoDB CRUD operations.
    This is the ONLY class you ever need to interact with.
    """

    def __init__(self, table_name: str, region_name: str) -> None:
        self.table_name = table_name
        self.client = get_dynamodb_client(region_name)

    def create_item(self, item: Dict[str, Any]) -> None:
        self.client.put_item(TableName=self.table_name, Item=self._serialize(item))

    def get_item(self, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        response = self.client.get_item(TableName=self.table_name, Key=self._serialize(key))
        return self._deserialize(response.get("Item"))

    def update_item(
        self,
        key: Dict[str, Any],
        update_expression: str,
        expression_values: Dict[str, Any],
        expression_names: Optional[Dict[str, str]] = None,
    ) -> None:
        params = {
            "TableName": self.table_name,
            "Key": self._serialize(key),
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": self._serialize(expression_values),
        }

        if expression_names:
            params["ExpressionAttributeNames"] = expression_names

        self.client.update_item(**params)

    def delete_item(self, key: Dict[str, Any]) -> None:
        self.client.delete_item(TableName=self.table_name, Key=self._serialize(key))

    def _serialize(self, data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Converts normal Python dict → DynamoDB format.
        """
        dynamodb_item = {}

        for k, v in data.items():
            if isinstance(v, str):
                dynamodb_item[k] = {"S": v}
            elif isinstance(v, bool):
                dynamodb_item[k] = {"BOOL": v}
            elif isinstance(v, int):
                dynamodb_item[k] = {"N": str(v)}
            elif isinstance(v, float):
                dynamodb_item[k] = {"N": str(v)}
            elif v is None:
                dynamodb_item[k] = {"NULL": True}
            else:
                raise ValueError(f"Unsupported type for {k}: {type(v)}")

        return dynamodb_item

    def _deserialize(self, item: Optional[Dict[str, Dict[str, Any]]]):
        if not item:
            return None

        python_item = {}

        for k, v in item.items():
            dtype = list(v.keys())[0]
            value = v[dtype]

            if dtype == "S":
                python_item[k] = value
            elif dtype == "N":
                python_item[k] = int(value) if value.isdigit() else float(value)
            elif dtype == "BOOL":
                python_item[k] = value
            elif dtype == "NULL":
                python_item[k] = None
            else:
                python_item[k] = value

        return python_item
