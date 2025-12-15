"""
Test script to verify if the FastAPI app works correctly with Mangum for Lambda.
This simulates a mock API Gateway event for the get_user endpoint.
"""

import json
import os
import sys

# Add the parent directory to sys.path to import auth_service
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from auth_service.main import mangum_handler


def test_lambda():
    # Mock API Gateway event for GET /users/{user_id}
    mock_event = {
        "version": "2.0",
        "routeKey": "GET /users/{user_id}",
        "rawPath": "/users/example_user_id",
        "rawQueryString": "",
        "headers": {"authorization": "Bearer your_token_here"},  # Replace with a valid token
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "/users/example_user_id",
                "protocol": "HTTP/1.1",
                "sourceIp": "127.0.0.1",
                "userAgent": "test-agent",
            }
        },
        "pathParameters": {"user_id": "example_user_id"},
        "body": None,
        "isBase64Encoded": False,
    }

    # Mock Lambda context
    mock_context = {
        "function_name": "test-function",
        "function_version": "$LATEST",
        "invoked_function_arn": "arn:aws:lambda:us-east-1:123456789012:function:test-function",
        "memory_limit_in_mb": 128,
        "aws_request_id": "12345678-1234-1234-1234-123456789012",
        "log_group_name": "/aws/lambda/test-function",
        "log_stream_name": "2023/01/01/[$LATEST]abcd1234",
    }

    # Call the Mangum handler
    response = mangum_handler(event=mock_event, context=mock_context)  # type: ignore

    # Print the response
    print("Lambda Response:")
    print(json.dumps(response, indent=2))

    # Check if statusCode is 200 (or expected)
    if response.get("statusCode") == 200:
        print("Test passed: App is working as Lambda.")
    else:
        print("Test failed: Check the response for errors.")


if __name__ == "__main__":
    test_lambda()
