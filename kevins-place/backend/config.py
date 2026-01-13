"""
KEVIN's Place - Configuration

Environment-based settings for the backend.
"""

import os
import secrets


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

# Security
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
CHALLENGE_EXPIRY_MINUTES = 5

# CORS (configure these for production)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Application
APP_NAME = "KEVIN's Place API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "A forum for all minds: Human, AI, and Hybrid"
