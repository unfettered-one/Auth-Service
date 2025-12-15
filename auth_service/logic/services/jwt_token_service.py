"""
Service for handling JWT token generation, verification, revocation, and rotation.
"""

import jwt
from datetime import datetime, timedelta, UTC

from auth_service.models.users import User
from auth_service.logic.interfaces.itoken_service import ITokenService


class JWTTokenService(ITokenService):
    """
    JWT Token Service implementation
    """

    def __init__(
        self,
        secret_key: str,
        access_token_expiry_minutes: int = 15,
        refresh_token_expiry_days: int = 7,
        algorithm: str = "HS256",
        revoked_tokens_store=None,  # TODO: Replace with proper interface for revoked tokens storage that is TTL-aware
    ):
        """
        Initialize the JWT Token Service.
        :param secret_key: Secret key for signing tokens.
        :param access_token_expiry_minutes: Expiry time for access tokens in minutes.
        :param refresh_token_expiry_days: Expiry time for refresh tokens in days.
        :param algorithm: Signing algorithm.
        :param revoked_tokens_store: Store for revoked tokens.
        """
        self.secret_key = secret_key
        self.access_exp = access_token_expiry_minutes
        self.refresh_exp = refresh_token_expiry_days
        self.algorithm = algorithm

        # Fallback to in-memory dict if nothing is provided
        self.revoked_tokens = revoked_tokens_store or set()

    async def generate_access_token(self, user: User) -> str:
        """
        Generate an access token for the given user.
        """
        payload = {
            "sub": user.id,
            "apps": user.apps,
            "email": user.email,
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(minutes=self.access_exp),
            "iat": datetime.now(UTC),
        }
        return jwt.encode(payload=payload, key=self.secret_key, algorithm=self.algorithm)

    async def generate_refresh_token(self, user: User) -> str:
        """
        Generate a refresh token for the given user.
        """
        payload = {
            "sub": user.id,
            "type": "refresh",
            "apps": user.apps,
            "email": user.email,
            "exp": datetime.now(UTC) + timedelta(days=self.refresh_exp),
            "iat": datetime.now(UTC),
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    async def verify_access_token(self, token: str) -> dict | None:
        """
        Verify the given access token and return its payload if valid.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "access":
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def verify_refresh_token(self, token: str) -> dict | None:
        """
        Verify the given refresh token and return its payload if valid.
        """
        # If token is revoked → instantly invalid
        if token in self.revoked_tokens:
            return None

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "refresh":
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def revoke_refresh_token(self, token: str) -> None:
        """Mark the refresh token as unusable."""
        await self.verify_refresh_token(token)
        self.revoked_tokens.add(token)

    async def rotate_refresh_token(self, old_token: str) -> str | None:
        """Revoke old refresh token and create a new one."""
        payload = await self.verify_refresh_token(old_token)
        if not payload:
            return None

        # revoke old token
        await self.revoke_refresh_token(old_token)

        # create new refresh token for same user
        user_id = payload["sub"]
        user = User(
            id=user_id, email=payload.get("email", ""), name=None, password_hash="", apps=payload.get("apps", [])
        )
        return await self.generate_refresh_token(user)
