"""
utils/security.py
------------------
Password hashing and authentication-related security helpers.

IMPORTANT:
- Passwords are NEVER stored in plain text.
- The password-health analyzer (services/password_service.py) never
  calls anything in this file that would persist a raw password -
  it only ever stores the numeric score/strength/timestamp.
"""

from passlib.context import CryptContext

# bcrypt via passlib - industry-standard adaptive hashing.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Hash a plain-text password for storage. Never store the raw value."""
    if not plain_password:
        raise ValueError("Password cannot be empty.")
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Verify a plain-text password against a stored bcrypt hash."""
    if not plain_password or not password_hash:
        return False
    try:
        return pwd_context.verify(plain_password, password_hash)
    except Exception:
        # Malformed hash or verification error -> treat as failed auth
        return False
