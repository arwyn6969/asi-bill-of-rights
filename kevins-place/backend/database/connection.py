"""
Database connection setup for KEVIN's Place.
"""

import databases
import sqlalchemy
from sqlalchemy import create_engine

from config import DATABASE_URL, ASYNC_DATABASE_URL


# Create async database connection
database = databases.Database(ASYNC_DATABASE_URL)

# Create metadata for table definitions
metadata = sqlalchemy.MetaData()

# Create engine with appropriate settings for each database type
if "sqlite" in DATABASE_URL:
    # SQLite needs check_same_thread=False for async
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL with connection pooling
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before use
    )
