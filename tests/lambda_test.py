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

    # Mock context (minimal)
    mock_context = {}

    # Call the Mangum handler
    response = mangum_handler(mock_event, mock_context)

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
