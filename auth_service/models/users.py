from pydantic import Field, EmailStr
from auth_service.models.base import BaseModelForbidExtra
from datetime import datetime, UTC


class User(BaseModelForbidExtra):
    id: str
    name: str | None = None
    email: EmailStr
    password_hash: str = Field(...)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    apps: list[str] = []


class UserRequest(BaseModelForbidExtra):
    name: str | None = None
    email: EmailStr
    password: str
    app_name: str


class UserResponse(BaseModelForbidExtra):
    id: str
    name: str | None = None
    email: EmailStr
    apps: list[str]
