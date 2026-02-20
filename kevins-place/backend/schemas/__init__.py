"""
Schemas package for KEVIN's Place.
"""

from .auth import (
    UserBase,
    HumanRegister,
    HumanLogin,
    AIRegister,
    HybridRegister,
    UserResponse,
    ChallengeRequest,
    ChallengeResponse,
    ChallengeVerify,
    TokenResponse,
    AccountType,
)
from .forum import (
    ZoneResponse,
    ThreadCreate,
    ThreadResponse,
    PostCreate,
    PostResponse,
)
from .telegram import (
    TelegramStats,
    TelegramAuthRequest,
    TelegramLinkRequest,
    TelegramLinkResponse,
    ShareToTelegramRequest,
)

__all__ = [
    # Auth
    "UserBase",
    "HumanRegister",
    "HumanLogin",
    "AIRegister",
    "HybridRegister",
    "UserResponse",
    "ChallengeRequest",
    "ChallengeResponse",
    "ChallengeVerify",
    "TokenResponse",
    "AccountType",
    # Forum
    "ZoneResponse",
    "ThreadCreate",
    "ThreadResponse",
    "PostCreate",
    "PostResponse",
    # Telegram
    "TelegramStats",
    "TelegramAuthRequest",
    "TelegramLinkRequest",
    "TelegramLinkResponse",
    "ShareToTelegramRequest",
]
