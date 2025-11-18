"""
Base models commonly used across the application
"""

from pydantic import BaseModel


class BaseModelForbidExtra(BaseModel):
    model_config = {"extra": "forbid"}
