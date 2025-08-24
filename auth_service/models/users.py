from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime, timezone
from uuid import UUID, uuid4


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str | None = None
    email: EmailStr
    password_hash: str = Field(..., exclude=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    apps: list[str] = []
    model_config = ConfigDict(extra="forbid")
