"""
Helper functions to manage password hashing and verification.
"""

import bcrypt


async def hash_password(password: str) -> str:
    """
    util to hash the password
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    util to verify the password
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
