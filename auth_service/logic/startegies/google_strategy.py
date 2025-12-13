"""
Strategy for Google authentication.
"""

from logic.interfaces.iauth_strategy import IAuthStrategy
from logic.repository.json_user_repository import IUserRepository
from models.users import User

from google.oauth2 import id_token
from google.auth.transport import requests

from utils.helper import generate_user_id
from auth_service.configuration import settings

from errorhub.exceptions import NotFoundException, ForbiddenException
from errorhub.models import ErrorSeverity


class GoogleAuthStrategy(IAuthStrategy):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
        # TODO add audience validation after setting up OAuth client IDs from fronend side

    async def authenticate(self, credentials: dict) -> User:
        google_token = credentials.get("id_token")

        if not google_token:
            raise NotFoundException(
                service="Auth Service",
                message="Google ID token not found",
                severity=ErrorSeverity.MEDIUM,
                environment=settings.get_environment(),
                context={
                    "detail": f"Google ID token is missing in credentials.",
                    "suggestion": "Please provide a valid Google ID token",
                },
            )

        # Verify Google token
        try:
            payload = id_token.verify_oauth2_token(google_token, requests.Request())
        except Exception:
            raise ForbiddenException(
                service="Auth Service",
                message="Invalid Google ID token",
                severity=ErrorSeverity.LOW,
                environment=settings.get_environment(),
                context={
                    "detail": "Google ID token verification failed.",
                    "suggestion": "Please provide a valid Google ID token",
                },
            )

        email = payload["email"]
        name = payload.get("name")

        # Fetch or create user
        user = await self.user_repository.get_user_by_email(email)

        if not user:
            user = User(
                id=await generate_user_id(),
                email=email,
                name=name,
                password_hash="",
                apps=[],
            )
            await self.user_repository.create_user(user)

        return user
