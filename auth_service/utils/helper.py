"""
Common helper functions for the authentication service.
"""

import uuid


async def generate_user_id() -> str:
    """Generate a unique user ID."""

    return str(uuid.uuid4())
