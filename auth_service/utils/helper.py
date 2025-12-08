"""
Common helper functions for the authentication service.
"""

import uuid

from errorhub.models import ErrorSeverity
from errorhub.exceptions import ForbiddenException

from configuration import settings


async def generate_user_id() -> str:
    """Generate a unique user ID."""

    return str(uuid.uuid4())


async def validate_user_with_token(user_id: str, token_data: dict, refresh: bool = False) -> bool:
    """Validate if the user ID matches the token's user ID."""

    if refresh:
        return user_id == token_data.get("sub") and token_data.get("type") == "refresh"
    return user_id == token_data.get("sub") and token_data.get("type") == "access"


async def raise_exception_if_not_valid_user(user_id: str, token_data: dict, refresh: bool = False):
    """Raise ForbiddenException if the user is not valid."""

    is_valid = await validate_user_with_token(user_id, token_data, refresh)
    if not is_valid:
        raise ForbiddenException(
            service="Auth Service",
            message="User validation failed",
            severity=ErrorSeverity.LOW,
            environment=settings.get_environment(),
            context={
                "detail": "The user ID does not match the token's user ID or token type is invalid.",
                "suggestion": "Please provide valid credentials.",
            },
        )
