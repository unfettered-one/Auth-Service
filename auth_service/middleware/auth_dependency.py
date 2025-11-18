# TODO to be moved to a common package later so that all service can use it

from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from logic.services.jwt_token_service import JWTTokenService
from configuration import settings

bearer_scheme = HTTPBearer(auto_error=False)

# Create a standalone token service instance (no factory)
token_service = JWTTokenService(
    secret_key=settings.get_jwt_secret() or "default_secret_key",
    access_token_expiry_minutes=15,
    refresh_token_expiry_days=7,
)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    """
    Validates Access Token independently using JWTTokenService.
    This file has ZERO dependency on AuthenticationService or Factory,
    so it can be moved to a shared library later.
    """
    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    token = credentials.credentials  # Already extracted by HTTPBearer

    # Verify JWT access token directly
    payload = await token_service.verify_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")

    return payload  # <-- becomes current_user
