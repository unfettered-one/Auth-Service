from fastapi import Security
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
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    if credentials is None:
        raise BadRequestException(
            service="Auth Service",
            message="Authorization header missing",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "No Authorization header provided.",
            },
        )

    token = credentials.credentials

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

    return payload
