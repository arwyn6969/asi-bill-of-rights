"""
Routers package for KEVIN's Place.
"""

from .auth import router as auth_router
from .zones import router as zones_router
from .threads import router as threads_router
from .posts import router as posts_router
from .search import router as search_router
from .telegram import router as telegram_router

__all__ = [
    "auth_router",
    "zones_router",
    "threads_router",
    "posts_router",
    "search_router",
    "telegram_router",
]
