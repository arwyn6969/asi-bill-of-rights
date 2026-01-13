"""
Authentication services: JWT, password hashing, and utilities.
"""

import json
import uuid
import base64
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Optional

from config import SECRET_KEY


def generate_uuid() -> str:
    """Generate a UUID."""
    return str(uuid.uuid4())


def hash_password(password: str) -> str:
    """Hash a password using SHA-256 with secret key."""
    return hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == password_hash


def create_jwt(user_id: str, account_type: str) -> str:
    """Create a simple JWT-like token.
    
    Note: This is a custom implementation. Consider using python-jose
    for production.
    """
    payload = {
        "user_id": user_id,
        "account_type": account_type,
        "exp": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    }
    payload_str = json.dumps(payload)
    token = base64.b64encode(payload_str.encode()).decode()
    signature = hashlib.sha256((token + SECRET_KEY).encode()).hexdigest()[:16]
    return f"{token}.{signature}"


def decode_jwt(token: str) -> Optional[dict]:
    """Decode and verify a JWT-like token.
    
    Returns None if token is invalid or expired.
    """
    try:
        parts = token.split(".")
        if len(parts) != 2:
            return None
        
        payload_b64, signature = parts
        expected_sig = hashlib.sha256((payload_b64 + SECRET_KEY).encode()).hexdigest()[:16]
        
        if signature != expected_sig:
            return None
        
        payload_str = base64.b64decode(payload_b64).decode()
        payload = json.loads(payload_str)
        
        # Check expiry
        exp = datetime.fromisoformat(payload["exp"])
        if datetime.now(timezone.utc) > exp:
            return None
        
        return payload
    except Exception:
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
