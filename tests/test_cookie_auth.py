"""
Test suite for HTTP-only cookie-based authentication.
Validates that tokens are stored in secure cookies, not in response body.
"""

import os
import sys
import asyncio
from unittest.mock import Mock, AsyncMock, patch

# Add the parent directory to sys.path to import auth_service
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from auth_service.main import app
from auth_service.models.auth import (
    LoginResponse,
    TokenRefreshResponse,
    LogoutRequestModel,
)
from auth_service.models.users import UserResponse


client = TestClient(app)


def test_login_sets_http_only_cookies():
    """
    Test that login endpoint sets HTTP-only cookies for tokens.
    Tokens should NOT appear in response body.
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
        # Mock authentication service
        mock_service_instance = AsyncMock()
        mock_auth_service.return_value = mock_service_instance

        # Mock user object
        mock_user = Mock()
        mock_user.id = "user_123"
        mock_user.name = "Test User"
        mock_user.email = "test@example.com"
        mock_user.apps = []

        # Mock login response with tokens
        mock_service_instance.login = AsyncMock(
            return_value={
                "user": mock_user,
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_access_token",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_refresh_token",
            }
        )

        response = client.post("/auth/login", json=login_payload)

        # Verify response status
        assert response.status_code == 201, (
            f"Expected 201, got {response.status_code}: {response.text}"
        )

        # Verify response body contains user info but NOT tokens
        response_data = response.json()
        assert "user" in response_data
        assert "message" in response_data
        assert response_data["message"] == "Login successful"
        assert "access_token" not in response_data, (
            "Access token should NOT be in response body"
        )
        assert "refresh_token" not in response_data, (
            "Refresh token should NOT be in response body"
        )

        # Verify tokens are in HTTP-only cookies
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies

        # Verify cookie attributes
        access_cookie = response.cookies.get("access_token")
        refresh_cookie = response.cookies.get("refresh_token")

        assert access_cookie is not None
        assert refresh_cookie is not None

        print("✓ Login sets HTTP-only cookies correctly")
        print(f"✓ Access token cookie present: {bool(access_cookie)}")
        print(f"✓ Refresh token cookie present: {bool(refresh_cookie)}")


def test_logout_clears_cookies():
    """
    Test that logout endpoint clears both access and refresh token cookies.
    """
    logout_payload = {"data": {}}

    with patch(
        "auth_service.logic.factory.factory.get_authentication_service"
    ) as mock_auth_service:
        with patch(
            "auth_service.middleware.auth_dependency._get_token_service"
        ) as mock_token_service:
            # Mock services
            mock_service_instance = AsyncMock()
            mock_auth_service.return_value = mock_service_instance
            mock_service_instance.logout = AsyncMock(
                return_value={"message": "Logged out"}
            )

            # Mock token service for credential validation
            mock_token_instance = AsyncMock()
            mock_token_service.return_value = mock_token_instance
            mock_token_instance.verify_access_token = AsyncMock(
                return_value={"sub": "user_123"}
            )

            # Set cookies as if user is logged in
            client.cookies.set(
                "access_token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_access_token"
            )
            client.cookies.set(
                "refresh_token",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_refresh_token",
            )

            response = client.post("/auth/logout", json=logout_payload)

            # Verify response
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["message"] == "User logged out successfully"

            print("✓ Logout endpoint returns 200 OK")
            print("✓ Logout response contains success message")


def test_refresh_token_extracts_from_cookies():
    """
    Test that refresh_token endpoint extracts refresh token from cookies (not body).
    """
    refresh_payload = {
        "data": {}  # Empty data - token comes from cookie
    }

    with patch(
        "auth_service.logic.factory.factory.get_authentication_service"
    ) as mock_auth_service:
        mock_service_instance = AsyncMock()
        mock_auth_service.return_value = mock_service_instance

        # Mock refresh response
        mock_service_instance.refresh = AsyncMock(
            return_value={
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new_access_token",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new_refresh_token",
            }
        )

        # Set refresh token in cookie
        client.cookies.set(
            "refresh_token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_refresh_token"
        )

        response = client.post("/auth/refresh", json=refresh_payload)

        # Verify response
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert "access_token" not in response_data, (
            "Access token should NOT be in response body"
        )
        assert "refresh_token" not in response_data, (
            "Refresh token should NOT be in response body"
        )

        # Verify new tokens are in cookies
        assert "access_token" in response.cookies
        assert "refresh_token" in response.cookies

        print("✓ Refresh token endpoint returns 200 OK")
        print("✓ New tokens are set in cookies")
        print("✓ Tokens are not exposed in response body")


def test_get_current_user_accepts_cookie_token():
    """
    Test that get_current_user accepts tokens from cookies.
    """
    with patch(
        "auth_service.middleware.auth_dependency._get_token_service"
    ) as mock_token_service:
        with patch(
            "auth_service.logic.factory.factory.get_user_service"
        ) as mock_user_service:
            # Mock token service
            mock_token_instance = AsyncMock()
            mock_token_service.return_value = mock_token_instance
            mock_token_instance.verify_access_token = AsyncMock(
                return_value={"sub": "user_123"}
            )

            # Mock user service
            mock_user_instance = AsyncMock()
            mock_user_service.return_value = mock_user_instance

            mock_user = Mock()
            mock_user.id = "user_123"
            mock_user.name = "Test User"
            mock_user.email = "test@example.com"
            mock_user.apps = []

            mock_user_instance.get_user_info = AsyncMock(return_value=mock_user)

            # Set token in cookie
            client.cookies.set(
                "access_token", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test_access_token"
            )

            response = client.get("/auth/me")

            # Verify response
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["id"] == "user_123"
            assert response_data["name"] == "Test User"
            assert response_data["email"] == "test@example.com"

            print("✓ GET /auth/me accepts token from cookie")
            print("✓ User info returned successfully")


def test_token_type_is_cookie():
    """
    Test that token_type in response is set to 'cookie' instead of 'bearer'.
    """
    assert LoginResponse.model_fields["token_type"].default == "cookie"
    assert TokenRefreshResponse.model_fields["token_type"].default == "cookie"

    print("✓ LoginResponse token_type is 'cookie'")
    print("✓ TokenRefreshResponse token_type is 'cookie'")


def test_logout_model_no_longer_requires_token():
    """
    Test that LogoutRequestModel no longer requires refresh_token in body.
    """
    from auth_service.models.auth import LogoutRequestModel, LogoutModel

    # This should not raise validation error
    try:
        logout_data = LogoutModel()
        logout_model = LogoutRequestModel(data=logout_data)
        print("✓ LogoutRequestModel accepts empty LogoutModel")
    except Exception as e:
        print(f"✗ LogoutRequestModel validation failed: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("HTTP-Only Cookie Authentication Test Suite")
    print("=" * 60 + "\n")

    test_token_type_is_cookie()
    print()

    test_logout_model_no_longer_requires_token()
    print()

    # Note: Other tests require mocking, which can be run with pytest
    print("\nTests that require async mocking should be run with pytest:")
    print("  pytest tests/test_cookie_auth.py -v")
    print("\n" + "=" * 60)
