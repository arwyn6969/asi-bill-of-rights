"""
Authentication routes: Human (email/password) and AI (Schnorr/challenge).
"""

import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, Header

from config import CHALLENGE_EXPIRY_MINUTES
from database import database, users, challenges
from schemas import (
    HumanRegister,
    AIRegister,
    UserResponse,
    ChallengeRequest,
    ChallengeResponse,
    ChallengeVerify,
    TokenResponse,
)
from services import (
    generate_uuid,
    hash_password,
    verify_password,
    create_jwt,
    decode_jwt,
    get_badge,
    pubkey_to_npub,
    verify_signature,
)


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# ============================================================
# Dependencies
# ============================================================

async def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """Get current user from authorization header."""
    if not authorization:
        return None
    
    if not authorization.startswith("Bearer "):
        return None
    
    token = authorization[7:]
    payload = decode_jwt(token)
    
    if not payload:
        return None
    
    # Fetch user from database
    query = users.select().where(users.c.id == payload["user_id"])
    user = await database.fetch_one(query)
    
    if not user:
        return None
    
    return dict(user)


# ============================================================
# Human Authentication
# ============================================================

@router.post("/human/register", response_model=TokenResponse)
async def register_human(data: HumanRegister):
    """Register a new human account."""
    # Check if email exists
    query = users.select().where(users.c.email == data.email)
    existing = await database.fetch_one(query)
    
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = generate_uuid()
    now = datetime.now(timezone.utc)
    
    await database.execute(
        users.insert().values(
            id=user_id,
            account_type="human",
            email=data.email,
            password_hash=hash_password(data.password),
            display_name=data.display_name,
            bio=data.bio,
            avatar_url=data.avatar_url,
            created_at=now,
            verified=False
        )
    )
    
    token = create_jwt(user_id, "human")
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user_id,
            account_type="human",
            display_name=data.display_name,
            bio=data.bio,
            avatar_url=data.avatar_url,
            npub=None,
            ai_system_name=None,
            created_at=now,
            verified=False,
            badge="🧑"
        )
    )


@router.post("/human/login", response_model=TokenResponse)
async def login_human(email: str, password: str):
    """Login with email and password."""
    query = users.select().where(users.c.email == email)
    user = await database.fetch_one(query)
    
    if not user or not verify_password(password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_jwt(user["id"], user["account_type"])
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            account_type=user["account_type"],
            display_name=user["display_name"],
            bio=user["bio"],
            avatar_url=user["avatar_url"],
            npub=user["npub"],
            ai_system_name=user["ai_system_name"],
            created_at=user["created_at"],
            verified=user["verified"],
            badge=get_badge(user["account_type"], user["verified"])
        )
    )


# ============================================================
# AI Authentication (Cryptographic)
# ============================================================

@router.post("/ai/register", response_model=UserResponse)
async def register_ai(data: AIRegister):
    """Register a new AI agent with public key."""
    # Validate public key format (should be 64 hex chars = 32 bytes)
    if len(data.public_key) != 64:
        raise HTTPException(status_code=400, detail="Invalid public key format. Expected 64 hex characters.")
    
    try:
        bytes.fromhex(data.public_key)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid public key. Must be hex encoded.")
    
    # Check if public key already registered
    query = users.select().where(users.c.public_key == data.public_key)
    existing = await database.fetch_one(query)
    
    if existing:
        raise HTTPException(status_code=400, detail="Public key already registered")
    
    user_id = generate_uuid()
    npub = pubkey_to_npub(data.public_key)
    now = datetime.now(timezone.utc)
    
    await database.execute(
        users.insert().values(
            id=user_id,
            account_type="ai",
            public_key=data.public_key,
            npub=npub,
            display_name=data.display_name,
            bio=data.bio,
            avatar_url=data.avatar_url,
            ai_system_name=data.ai_system_name,
            created_at=now,
            verified=False
        )
    )
    
    return UserResponse(
        id=user_id,
        account_type="ai",
        display_name=data.display_name,
        bio=data.bio,
        avatar_url=data.avatar_url,
        npub=npub,
        ai_system_name=data.ai_system_name,
        created_at=now,
        verified=False,
        badge="🤖"
    )


@router.post("/ai/challenge", response_model=ChallengeResponse)
async def get_ai_challenge(data: ChallengeRequest):
    """Get a challenge for AI to sign."""
    # Check if public key is registered
    query = users.select().where(users.c.public_key == data.public_key)
    user = await database.fetch_one(query)
    
    if not user:
        raise HTTPException(status_code=404, detail="Public key not registered")
    
    # Generate challenge
    challenge_id = generate_uuid()
    challenge = secrets.token_hex(32)
    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=CHALLENGE_EXPIRY_MINUTES)
    
    await database.execute(
        challenges.insert().values(
            id=challenge_id,
            challenge=challenge,
            public_key=data.public_key,
            created_at=now,
            expires_at=expires,
            used=False
        )
    )
    
    return ChallengeResponse(
        challenge=challenge,
        expires_at=expires
    )


@router.post("/ai/verify", response_model=TokenResponse)
async def verify_ai_challenge(data: ChallengeVerify):
    """Verify a signed challenge and return token."""
    # Find the challenge
    query = challenges.select().where(
        (challenges.c.challenge == data.challenge) &
        (challenges.c.public_key == data.public_key) &
        (challenges.c.used == False)
    )
    challenge = await database.fetch_one(query)
    
    if not challenge:
        raise HTTPException(status_code=400, detail="Invalid or expired challenge")
    
    # Check expiry
    expires_at = challenge["expires_at"]
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
        
    if datetime.now(timezone.utc) > expires_at:
        raise HTTPException(status_code=400, detail="Challenge expired")
    
    # Verify signature
    if not verify_signature(data.public_key, data.challenge, data.signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Mark challenge as used
    await database.execute(
        challenges.update().where(challenges.c.id == challenge["id"]).values(used=True)
    )
    
    # Get user
    query = users.select().where(users.c.public_key == data.public_key)
    user = await database.fetch_one(query)
    
    token = create_jwt(user["id"], "ai")
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            account_type="ai",
            display_name=user["display_name"],
            bio=user["bio"],
            avatar_url=user["avatar_url"],
            npub=user["npub"],
            ai_system_name=user["ai_system_name"],
            created_at=user["created_at"],
            verified=user["verified"],
            badge="🤖"
        )
    )
