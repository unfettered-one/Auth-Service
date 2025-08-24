from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime, UTC


class User(BaseModel):
    id: str
    name: str | None = None
    email: EmailStr
    password_hash: str = Field(...)
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    apps: list[str] = []
    model_config = ConfigDict(extra="forbid")


class UserRequest(BaseModel):
    name: str | None = None
    email: EmailStr
    password: str
    app_name: str
    model_config = ConfigDict(extra="forbid")
