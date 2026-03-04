"""
Cookie management utilities for authentication
"""

from fastapi.responses import ORJSONResponse
from auth_service.configuration import settings


def get_cookie_config() -> dict:
    """Get common cookie configuration"""
    return {
        "httponly": True,
        "secure": settings.get_cookie_secure_flag(),
        "samesite": settings.cookie_samesite(),
        "path": "/",
    }


def set_auth_cookies(response: ORJSONResponse, access_token: str, refresh_token: str) -> ORJSONResponse:
    """Set both access and refresh token cookies on response"""
    cookie_config = get_cookie_config()

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=settings.access_token_expiry_seconds(),
        **cookie_config,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=settings.refresh_token_expiry_seconds(),
        **cookie_config,
    )

    return response


def clear_auth_cookies(response: ORJSONResponse) -> ORJSONResponse:
    """Clear both access and refresh token cookies from response"""
    cookie_config = get_cookie_config()

    response.delete_cookie(key="access_token", **cookie_config)
    response.delete_cookie(key="refresh_token", **cookie_config)

    return response
