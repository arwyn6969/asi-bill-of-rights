"""
Authentication services: JWT (PyJWT + HS256), password hashing (bcrypt), and utilities.
"""

import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional

import jwt
import bcrypt

from config import SECRET_KEY


def generate_uuid() -> str:
    """Generate a UUID."""
    return str(uuid.uuid4())


def hash_password(password: str) -> str:
    """Hash a password using bcrypt (adaptive cost, salted)."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its bcrypt hash.
    
    Also accepts legacy SHA-256 hashes for backward compatibility during
    migration. Legacy users will be re-hashed on next login.
    """
    try:
        return bcrypt.checkpw(password.encode(), password_hash.encode())
    except (ValueError, TypeError):
        # Legacy SHA-256 hash — not bcrypt format.  Fall through to False
        # so the caller can handle migration if needed.
        import hashlib
        legacy = hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()
        return legacy == password_hash


def create_jwt(user_id: str, account_type: str) -> str:
    """Create a signed JWT token using HS256.
    
    Token contains user_id, account_type, and a 7-day expiry.
    """
    payload = {
        "user_id": user_id,
        "account_type": account_type,
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token: str) -> Optional[dict]:
    """Decode and verify a JWT token.
    
    Returns None if token is invalid, tampered, or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_badge(account_type: str, verified: bool = False) -> str:
    """Get emoji badge for account type."""
    if verified and account_type in ["human", "ai"]:
        return "✨"  # Verified
    
    badges = {
        "human": "🧑",
        "ai": "🤖",
        "hybrid": "🔀"
    }
    return badges.get(account_type, "❓")
