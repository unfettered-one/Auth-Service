from fastapi import Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from auth_service.logic.services.jwt_token_service import JWTTokenService
from auth_service.configuration import settings
from errorhub.exceptions import (
    UnauthorizedException,
    BadRequestException,
    InternalServerErrorException,
)
from errorhub.models import ErrorSeverity

bearer_scheme = HTTPBearer(auto_error=False)

_token_service: JWTTokenService | None = None


def _get_token_service() -> JWTTokenService:
    """
    Lazily create and cache JWTTokenService.
    """
    global _token_service

    if _token_service is None:
        secret_key = settings.get_jwt_secret()
        if not secret_key:
            raise InternalServerErrorException(
                service="Auth Service",
                message="JWT secret is not configured",
                severity=ErrorSeverity.HIGH,
                environment=settings.get_environment(),
                context={
                    "detail": "The JWT secret key is missing in the configuration.",
                },
            )

        _token_service = JWTTokenService(
            secret_key=secret_key,
            access_token_expiry_minutes=15,
            refresh_token_expiry_days=7,
        )

    return _token_service


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    """
    Extract access token from HTTP-only cookie (preferred) or Authorization header (fallback).
    Supports hybrid transition: new clients use cookies, legacy clients use Bearer header.
    """
    token = None
    token_source = None

    # Check HTTP-only cookie first (preferred)
    token = request.cookies.get("access_token")
    if token:
        token_source = "cookie"

    # # Fallback to Authorization header for User APIs
    if not token and credentials is not None:
        token = credentials.credentials
        token_source = "header"

    if not token:
        raise BadRequestException(
            service="Auth Service",
            message="Access token missing",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "No access token provided in cookies or Authorization header.",
            },
        )

    token_service = _get_token_service()

    payload = await token_service.verify_access_token(token)

    if not payload:
        raise UnauthorizedException(
            service="Auth Service",
            message="Invalid or expired access token",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "The provided access token is invalid or expired.",
            },
        )
    payload["_token_source"] = token_source
    return payload
