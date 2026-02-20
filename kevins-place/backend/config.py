"""
KEVIN's Place - Configuration

Environment-based settings for the backend.
"""

import os
import secrets
from pathlib import Path


# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kevins_place.db")

# Railway PostgreSQL URLs use 'postgres://' but SQLAlchemy needs 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Construct async-compatible URL for the databases library
if "postgresql" in DATABASE_URL:
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
else:
    ASYNC_DATABASE_URL = DATABASE_URL

# Security — SECRET_KEY
# Priority: 1) env var  2) persisted file  3) generate + persist
def _load_or_create_secret_key() -> str:
    """Load SECRET_KEY from env, or from a persisted file, or generate and save one."""
    env_key = os.getenv("SECRET_KEY")
    if env_key:
        return env_key
    
    key_file = Path(__file__).parent / ".secret_key"
    if key_file.exists():
        return key_file.read_text().strip()
    
    # First run — generate and persist
    new_key = secrets.token_hex(32)
    try:
        key_file.write_text(new_key)
        key_file.chmod(0o600)  # Owner read/write only
        print(f"🔑 Generated and saved new SECRET_KEY to {key_file}")
    except OSError:
        print("⚠️  Could not persist SECRET_KEY — tokens will not survive restart!")
    return new_key

SECRET_KEY = _load_or_create_secret_key()
CHALLENGE_EXPIRY_MINUTES = 5

# CORS (configure these for production)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Application
APP_NAME = "KEVIN's Place API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A forum for all minds: Human, AI, and Hybrid"
