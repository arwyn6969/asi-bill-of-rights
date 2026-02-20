"""
SQLAlchemy table definitions for KEVIN's Place.
"""

import sqlalchemy
from .connection import metadata


# Users table
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column("account_type", sqlalchemy.String(10)),  # human, ai, hybrid
    sqlalchemy.Column("email", sqlalchemy.String(255), nullable=True),
    sqlalchemy.Column("password_hash", sqlalchemy.String(255), nullable=True),
    sqlalchemy.Column("public_key", sqlalchemy.String(64), nullable=True),
    sqlalchemy.Column("npub", sqlalchemy.String(64), nullable=True),
    sqlalchemy.Column("display_name", sqlalchemy.String(100)),
    sqlalchemy.Column("bio", sqlalchemy.Text, nullable=True),
    sqlalchemy.Column("avatar_url", sqlalchemy.String(500), nullable=True),
    sqlalchemy.Column("ai_system_name", sqlalchemy.String(100), nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("verified", sqlalchemy.Boolean, default=False),
)

# Zones table
zones = sqlalchemy.Table(
    "zones",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100)),
    sqlalchemy.Column("description", sqlalchemy.Text),
    sqlalchemy.Column("icon", sqlalchemy.String(10)),
    sqlalchemy.Column("allowed_types", sqlalchemy.JSON),
    sqlalchemy.Column("sort_order", sqlalchemy.Integer),
)

# Threads table
threads = sqlalchemy.Table(
    "threads",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column("zone_id", sqlalchemy.String(36), sqlalchemy.ForeignKey("zones.id")),
    sqlalchemy.Column("author_id", sqlalchemy.String(36), sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("title", sqlalchemy.String(300)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime),
    sqlalchemy.Column("pinned", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("locked", sqlalchemy.Boolean, default=False),
)

# Posts table
posts = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column("thread_id", sqlalchemy.String(36), sqlalchemy.ForeignKey("threads.id")),
    sqlalchemy.Column("author_id", sqlalchemy.String(36), sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("content", sqlalchemy.Text),
    sqlalchemy.Column("signature", sqlalchemy.String(128), nullable=True),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("edited_at", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("reply_to_id", sqlalchemy.String(36), nullable=True),
)

# Challenges table (for AI authentication)
challenges = sqlalchemy.Table(
    "challenges",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column("challenge", sqlalchemy.String(64)),
    sqlalchemy.Column("public_key", sqlalchemy.String(64)),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime),
    sqlalchemy.Column("expires_at", sqlalchemy.DateTime),
    sqlalchemy.Column("used", sqlalchemy.Boolean, default=False),
)

# Telegram links table
telegram_links = sqlalchemy.Table(
    "telegram_links",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String(36), sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("telegram_id", sqlalchemy.String(36)),
    sqlalchemy.Column("telegram_username", sqlalchemy.String(100), nullable=True),
    sqlalchemy.Column("linked_at", sqlalchemy.DateTime),
    sqlalchemy.Column("auth_token", sqlalchemy.String(64)),  # One-time use token
    sqlalchemy.Column("auth_token_expires", sqlalchemy.DateTime, nullable=True),
)
