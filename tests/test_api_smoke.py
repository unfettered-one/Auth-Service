"""
API Smoke Testing - Validates all endpoints are reachable, return correct status codes,
and have proper response structure without crashing.
"""

import os
import sys
import time
from unittest.mock import Mock, AsyncMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from auth_service.main import app

client = TestClient(app)


def test_auth_login_endpoint_smoke():
    """
    Smoke test for POST /auth/login - validates endpoint is reachable and returns 201.
    """
    login_payload = {
        "data": {
            "strategy": "email_password",
            "credentials": {"email": "test@example.com", "password": "password123"},
        }
    }

    with patch(
        "auth_service.logic.factory.factory.get_authentication_service"
    ) as mock_auth_service:
        mock_service_instance = AsyncMock()
        mock_auth_service.return_value = mock_service_instance

        mock_user = Mock()
        mock_user.id = "user_123"
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        mock_user.apps = []

        mock_service_instance.login = AsyncMock(
            return_value={
                "user": mock_user,
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
            }
        )

        start_time = time.time()
        response = client.post("/auth/login", json=login_payload)
        latency = time.time() - start_time

        # Validate response
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        assert latency < 2.0, f"Latency {latency}s exceeds threshold of 2s"

        # Validate JSON structure
        data = response.json()
        assert "user" in data
        assert "message" in data
        assert "token_type" in data

        # Validate cookies are set
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies

        print(f"✓ POST /auth/login - Status 201 OK (latency: {latency:.3f}s)")


def test_auth_logout_endpoint_smoke():
    """
    Smoke test for POST /auth/logout - validates endpoint is reachable.
    """
    logout_payload = {"data": {}}

    with patch(
        "auth_service.logic.factory.factory.get_authentication_service"
    ) as mock_auth_service:
        with patch(
            "auth_service.middleware.auth_dependency._get_token_service"
        ) as mock_token_service:
            mock_service_instance = AsyncMock()
            mock_auth_service.return_value = mock_service_instance
            mock_service_instance.logout = AsyncMock()

            mock_token_instance = AsyncMock()
            mock_token_service.return_value = mock_token_instance
            mock_token_instance.verify_access_token = AsyncMock(
                return_value={"sub": "user_123"}
            )

            client.cookies.set("access_token", "test_access_token")
            client.cookies.set("refresh_token", "test_refresh_token")

            start_time = time.time()
            response = client.post("/auth/logout", json=logout_payload)
            latency = time.time() - start_time

            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}"
            )
            assert latency < 2.0, f"Latency {latency}s exceeds threshold"

            data = response.json()
            assert "message" in data

            print(f"✓ POST /auth/logout - Status 200 OK (latency: {latency:.3f}s)")


def test_auth_refresh_endpoint_smoke():
    """
    Smoke test for POST /auth/refresh - validates endpoint is reachable.
    """
    refresh_payload = {"data": {}}

    with patch(
        "auth_service.logic.factory.factory.get_authentication_service"
    ) as mock_auth_service:
        mock_service_instance = AsyncMock()
        mock_auth_service.return_value = mock_service_instance

        mock_service_instance.refresh = AsyncMock(
            return_value={
                "access_token": "new_access_token",
                "refresh_token": "new_refresh_token",
            }
        )

        client.cookies.set("refresh_token", "test_refresh_token")

        start_time = time.time()
        response = client.post("/auth/refresh", json=refresh_payload)
        latency = time.time() - start_time

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert latency < 2.0, f"Latency {latency}s exceeds threshold"

        data = response.json()
        assert "message" in data

        print(f"✓ POST /auth/refresh - Status 200 OK (latency: {latency:.3f}s)")


def test_auth_me_endpoint_smoke():
    """
    Smoke test for GET /auth/me - validates endpoint is reachable.
    """
    with patch(
        "auth_service.middleware.auth_dependency._get_token_service"
    ) as mock_token_service:
        with patch(
            "auth_service.logic.factory.factory.get_user_service"
        ) as mock_user_service:
            mock_token_instance = AsyncMock()
            mock_token_service.return_value = mock_token_instance
            mock_token_instance.verify_access_token = AsyncMock(
                return_value={"sub": "user_123"}
            )

            mock_user_instance = AsyncMock()
            mock_user_service.return_value = mock_user_instance

            mock_user = Mock()
            mock_user.id = "user_123"
            mock_user.name = "Test User"
            mock_user.email = "test@example.com"
            mock_user.apps = []

            mock_user_instance.get_user_info = AsyncMock(return_value=mock_user)

            client.cookies.set("access_token", "test_access_token")

            start_time = time.time()
            response = client.get("/auth/me")
            latency = time.time() - start_time

            assert response.status_code == 200, (
                f"Expected 200, got {response.status_code}"
            )
            assert latency < 2.0, f"Latency {latency}s exceeds threshold"

            data = response.json()
            assert "id" in data
            assert "email" in data

            print(f"✓ GET /auth/me - Status 200 OK (latency: {latency:.3f}s)")


def test_auth_me_without_token_returns_401():
    """
    Test that GET /auth/me returns 401 without token.
    """
    # Clear cookies
    client.cookies.clear()

    response = client.get("/auth/me")

    assert response.status_code in [400, 401], (
        f"Expected 400 or 401 for missing token, got {response.status_code}"
    )

    print(
        f"✓ GET /auth/me without token - Status {response.status_code} (auth enforced)"
    )



def test_response_json_is_valid():
    """
    Validate that all responses return valid JSON with proper structure.
    """
    login_payload = {
        "data": {
            "strategy": "email_password",
            "credentials": {"email": "test@example.com", "password": "password123"},
        }
    }

    with patch(
        "auth_service.logic.factory.factory.get_authentication_service"
    ) as mock_auth_service:
        mock_service_instance = AsyncMock()
        mock_auth_service.return_value = mock_service_instance

        mock_user = Mock()
        mock_user.id = "user_123"
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        mock_user.apps = []

        mock_service_instance.login = AsyncMock(
            return_value={
                "user": mock_user,
                "access_token": "test_access_token",
                "refresh_token": "test_refresh_token",
            }
        )

        response = client.post("/auth/login", json=login_payload)

        # Validate JSON is parseable
        try:
            data = response.json()
            assert isinstance(data, dict)
            print("✓ Response JSON is valid and properly structured")
        except Exception as e:
            raise AssertionError(f"Response JSON is invalid: {e}")
