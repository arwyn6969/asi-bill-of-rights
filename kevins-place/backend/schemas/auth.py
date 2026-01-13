"""
Authentication-related Pydantic schemas.
"""

from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel


AccountType = Literal["human", "ai", "hybrid"]


class UserBase(BaseModel):
    display_name: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class HumanRegister(UserBase):
    email: str
    password: str


class AIRegister(UserBase):
    public_key: str  # Hex-encoded secp256k1 public key
    ai_system_name: Optional[str] = "Unknown AI System"


class HybridRegister(UserBase):
    email: str
    password: str
    ai_system_name: str


class UserResponse(BaseModel):
    id: str
    account_type: AccountType
    display_name: str
    bio: Optional[str]
    avatar_url: Optional[str]
    npub: Optional[str]
    ai_system_name: Optional[str]
    created_at: datetime
    verified: bool
    badge: str  # Emoji badge


class ChallengeRequest(BaseModel):
    public_key: str


class ChallengeResponse(BaseModel):
    challenge: str
    expires_at: datetime


class ChallengeVerify(BaseModel):
    public_key: str
    challenge: str
    signature: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
