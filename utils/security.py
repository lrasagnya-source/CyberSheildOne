"""
utils/security.py
------------------
Password hashing and authentication-related security helpers.

IMPORTANT:
- Passwords are NEVER stored in plain text.
- Uses bcrypt directly instead of passlib.
"""

import bcrypt


def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password for storage.
    """
    if not plain_password:
        raise ValueError("Password cannot be empty.")

    # Generate bcrypt hash and return it as a string
    hashed = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Verify a plain-text password against a stored bcrypt hash.
    """
    if not plain_password or not password_hash:
        return False

    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            password_hash.encode("utf-8")
        )
    except (ValueError, TypeError):
        # Invalid hash or verification error
        return False