"""
utils/validators.py
--------------------
Shared input validation helpers used across authentication and
security modules (registration form, password checker, email
breach checker, URL checker, etc).
"""

import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def is_valid_email(email: str) -> bool:
    """Basic structural validation for email addresses."""
    if not email or len(email) > 254:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def is_valid_name(name: str) -> bool:
    """Full name must be non-empty and reasonably sized."""
    if not name:
        return False
    name = name.strip()
    return 2 <= len(name) <= 100


def password_meets_minimum_requirements(password: str) -> tuple[bool, str]:
    """
    Minimum bar required to REGISTER an account (separate from the
    detailed Password Health scoring module, which gives a 0-100 score).
    """
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    return True, "OK"


def passwords_match(password: str, confirm_password: str) -> bool:
    return password == confirm_password


def is_valid_url(url: str) -> bool:
    """Lightweight structural URL validation (not a safety check)."""
    if not url:
        return False
    pattern = re.compile(
        r"^(https?://)?"
        r"([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"
        r"(:\d+)?"
        r"(/[^\s]*)?$"
    )
    return bool(pattern.match(url.strip()))
