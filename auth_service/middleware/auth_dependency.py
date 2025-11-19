"""
Reusable JWT Authentication Dependency
-------------------------------------

This module validates Access Tokens using JWTTokenService.
It is intentionally independent of AuthenticationService and the Factory,
so it can be moved into a shared/common package and reused by any service.
"""

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from logic.services.jwt_token_service import JWTTokenService
from configuration import settings
from errorhub.exceptions import UnauthorizedException, BadRequestException
from errorhub.models import ErrorSeverity

# FastAPI bearer schema (adds correct OpenAPI security!)
bearer_scheme = HTTPBearer(auto_error=False)

# Standalone TokenService instance (no factory)
token_service = JWTTokenService(
    secret_key=settings.get_jwt_secret() or "default_secret_key",
    access_token_expiry_minutes=15,
    refresh_token_expiry_days=7,
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    """
    Extracts and validates the Access Token from the Authorization header.

    This function:
        ✓ Extracts Bearer token
        ✓ Verifies the JWT signature
        ✓ Checks expiry
        ✓ Returns the decoded JWT payload on success
        ✓ Raises HTTP 401 on failure

    RETURN VALUE:
        Payload dict from JWT, example:
        {
            "sub": "user_123",
            "email": "yash@example.com",
            "apps": ["todo"],
            "iat": ...,
            "exp": ...,
            "type": "access"
        }
    """

    # No Authorization header → not authenticated
    if credentials is None:
        raise BadRequestException(
            service="Auth Service",
            message="Authorization header missing",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "No Authorization header provided in the request.",
                "suggestion": "Please include a valid Authorization header with a Bearer token.",
            },
        )
    # Extract the raw token from header
    token = credentials.credentials

    # Validate JWT access token
    payload = await token_service.verify_access_token(token)

    # Invalid / expired / wrong type
    if not payload:
        raise UnauthorizedException(
            service="Auth Service",
            message="Invalid or expired access token",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "The provided access token is invalid or has expired.",
                "suggestion": "Please provide a valid access token.",
            },
        )

    return payload  # <-- returned as "current user"
