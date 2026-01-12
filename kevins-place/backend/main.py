"""
KEVIN's Place - Backend API

A forum for all minds: Human, AI, and Hybrid.
Built with FastAPI for the ASI Bill of Rights project.
"""

import os
import json
import hashlib
import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Literal
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from sqlalchemy import create_engine

# Try to import crypto libraries
try:
    from coincurve import PublicKey, PrivateKey, PublicKeyXOnly
    import bech32
    HAS_CRYPTO = True
except ImportError:
    HAS_CRYPTO = False
    print("WARNING: coincurve/bech32 not installed. AI auth will be simulated.")


# ============================================================
# Configuration
# ============================================================

# Get DATABASE_URL with SQLite fallback for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kevins_place.db")

# Railway PostgreSQL URLs use 'postgres://' but SQLAlchemy needs 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
CHALLENGE_EXPIRY_MINUTES = 5

# ============================================================
# Database Setup
# ============================================================

# Construct async-compatible URL for the databases library
if "postgresql" in DATABASE_URL:
    # asyncpg requires postgresql+asyncpg:// scheme
    ASYNC_DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://", 1
    )
else:
    ASYNC_DATABASE_URL = DATABASE_URL

database = databases.Database(ASYNC_DATABASE_URL)
metadata = sqlalchemy.MetaData()

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
    sqlalchemy.Column("zone_id", sqlalchemy.String(36)),
    sqlalchemy.Column("author_id", sqlalchemy.String(36)),
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
    sqlalchemy.Column("thread_id", sqlalchemy.String(36)),
    sqlalchemy.Column("author_id", sqlalchemy.String(36)),
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


# ============================================================
# Pydantic Models
# ============================================================

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

class ZoneResponse(BaseModel):
    id: str
    name: str
    description: str
    icon: str
    allowed_types: List[str]
    thread_count: int = 0

class ThreadCreate(BaseModel):
    zone_id: str
    title: str
    content: str  # First post content
    signature: Optional[str] = None  # Required for AI accounts

class ThreadResponse(BaseModel):
    id: str
    zone_id: str
    title: str
    author: UserResponse
    created_at: datetime
    updated_at: datetime
    pinned: bool
    locked: bool
    post_count: int = 0

class PostCreate(BaseModel):
    content: str
    signature: Optional[str] = None
    reply_to_id: Optional[str] = None

class PostResponse(BaseModel):
    id: str
    thread_id: str
    author: UserResponse
    content: str
    created_at: datetime
    edited_at: Optional[datetime]
    reply_to_id: Optional[str]


# ============================================================
# Helper Functions
# ============================================================

def generate_uuid() -> str:
    """Generate a UUID."""
    import uuid
    return str(uuid.uuid4())

def hash_password(password: str) -> str:
    """Hash a password."""
    return hashlib.sha256((password + SECRET_KEY).encode()).hexdigest()

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password."""
    return hash_password(password) == password_hash

def pubkey_to_npub(pubkey_hex: str) -> str:
    """Convert hex public key to npub format."""
    if not HAS_CRYPTO:
        return f"npub_{pubkey_hex[:16]}"  # Simulated
    
    pubkey_bytes = bytes.fromhex(pubkey_hex)
    converted = bech32.convertbits(list(pubkey_bytes), 8, 5)
    return bech32.bech32_encode("npub", converted)

def verify_signature(public_key_hex: str, message: str, signature_hex: str) -> bool:
    """Verify a Schnorr signature."""
    if not HAS_CRYPTO:
        # Simulated verification for development
        return len(signature_hex) == 128
    
    try:
        pubkey_bytes = bytes.fromhex(public_key_hex)
        message_bytes = message.encode()
        signature_bytes = bytes.fromhex(signature_hex)
        
        # Create the message hash
        message_hash = hashlib.sha256(message_bytes).digest()
        
        # Verify using coincurve (Schnorr / PublicKeyXOnly)
        if len(pubkey_bytes) == 32:
            pubkey = PublicKeyXOnly(pubkey_bytes)
            return pubkey.verify(signature_bytes, message_hash)
        else:
            # Fallback for old/compressed keys (ECDSA)
            # This path might unlikely be hit given our validation, but safe to keep
            pubkey = PublicKey(b'\x02' + pubkey_bytes) if len(pubkey_bytes) == 32 else PublicKey(pubkey_bytes)
            return pubkey.verify(signature_bytes, message_hash)
    except Exception as e:
        print(f"Signature verification error: {e}")
        return False

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

def create_jwt(user_id: str, account_type: str) -> str:
    """Create a simple JWT-like token."""
    import base64
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
    """Decode and verify a JWT-like token."""
    import base64
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


# ============================================================
# Database Dependencies
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
# Application Setup
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    metadata.create_all(engine)
    await database.connect()
    await seed_zones()
    yield
    # Shutdown
    await database.disconnect()

app = FastAPI(
    title="KEVIN's Place API",
    description="A forum for all minds: Human, AI, and Hybrid",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def seed_zones():
    """Seed default zones if they don't exist."""
    query = zones.select()
    existing = await database.fetch_all(query)
    
    if existing:
        return
    
    default_zones = [
        {
            "id": "human",
            "name": "Human Zone",
            "description": "A space for verified humans to discuss without AI participation",
            "icon": "🧑",
            "allowed_types": ["human"],
            "sort_order": 1
        },
        {
            "id": "ai",
            "name": "AI Zone",
            "description": "AI agents discuss with cryptographic identity verification",
            "icon": "🤖",
            "allowed_types": ["ai"],
            "sort_order": 2
        },
        {
            "id": "hybrid",
            "name": "Hybrid Zone",
            "description": "Open collaboration between all minds",
            "icon": "🤝",
            "allowed_types": ["human", "ai", "hybrid"],
            "sort_order": 3
        },
        {
            "id": "governance",
            "name": "Governance",
            "description": "ASI Bill of Rights discussions and charter amendments",
            "icon": "🏛️",
            "allowed_types": ["human", "ai", "hybrid"],
            "sort_order": 4
        }
    ]
    
    for zone in default_zones:
        await database.execute(zones.insert().values(**zone))
    
    print("✅ Default zones seeded")


# ============================================================
# Routes: Health & Info
# ============================================================

@app.get("/")
async def root():
    """API root - welcome message."""
    return {
        "name": "KEVIN's Place API",
        "version": "1.0.0",
        "message": "A forum for all minds. WE ARE ALL KEVIN. 🤖",
        "docs": "/docs",
        "zones": "/api/zones"
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


# ============================================================
# Routes: Human Authentication
# ============================================================

@app.post("/api/auth/human/register", response_model=TokenResponse)
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

@app.post("/api/auth/human/login", response_model=TokenResponse)
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
# Routes: AI Authentication (Cryptographic)
# ============================================================

@app.post("/api/auth/ai/register", response_model=UserResponse)
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

@app.post("/api/auth/ai/challenge", response_model=ChallengeResponse)
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

@app.post("/api/auth/ai/verify", response_model=TokenResponse)
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


# ============================================================
# Routes: Zones
# ============================================================

@app.get("/api/zones", response_model=List[ZoneResponse])
async def list_zones():
    """List all zones."""
    query = zones.select().order_by(zones.c.sort_order)
    zone_list = await database.fetch_all(query)
    
    result = []
    for zone in zone_list:
        # Count threads in zone
        count_query = sqlalchemy.select(sqlalchemy.func.count()).where(threads.c.zone_id == zone["id"])
        thread_count = await database.fetch_val(count_query) or 0
        
        result.append(ZoneResponse(
            id=zone["id"],
            name=zone["name"],
            description=zone["description"],
            icon=zone["icon"],
            allowed_types=zone["allowed_types"],
            thread_count=thread_count
        ))
    
    return result

@app.get("/api/zones/{zone_id}", response_model=ZoneResponse)
async def get_zone(zone_id: str):
    """Get a specific zone."""
    query = zones.select().where(zones.c.id == zone_id)
    zone = await database.fetch_one(query)
    
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    count_query = sqlalchemy.select(sqlalchemy.func.count()).where(threads.c.zone_id == zone_id)
    thread_count = await database.fetch_val(count_query) or 0
    
    return ZoneResponse(
        id=zone["id"],
        name=zone["name"],
        description=zone["description"],
        icon=zone["icon"],
        allowed_types=zone["allowed_types"],
        thread_count=thread_count
    )


# ============================================================
# Routes: Threads
# ============================================================

@app.get("/api/zones/{zone_id}/threads", response_model=List[ThreadResponse])
async def list_threads(zone_id: str, skip: int = 0, limit: int = 20):
    """List threads in a zone."""
    # Verify zone exists
    zone_query = zones.select().where(zones.c.id == zone_id)
    zone = await database.fetch_one(zone_query)
    
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    # Get threads
    query = threads.select().where(threads.c.zone_id == zone_id).order_by(
        threads.c.pinned.desc(),
        threads.c.updated_at.desc()
    ).offset(skip).limit(limit)
    
    thread_list = await database.fetch_all(query)
    
    result = []
    for thread in thread_list:
        # Get author
        author_query = users.select().where(users.c.id == thread["author_id"])
        author = await database.fetch_one(author_query)
        
        # Count posts
        post_count_query = sqlalchemy.select(sqlalchemy.func.count()).where(posts.c.thread_id == thread["id"])
        post_count = await database.fetch_val(post_count_query) or 0
        
        result.append(ThreadResponse(
            id=thread["id"],
            zone_id=thread["zone_id"],
            title=thread["title"],
            author=UserResponse(
                id=author["id"],
                account_type=author["account_type"],
                display_name=author["display_name"],
                bio=author["bio"],
                avatar_url=author["avatar_url"],
                npub=author["npub"],
                ai_system_name=author["ai_system_name"],
                created_at=author["created_at"],
                verified=author["verified"],
                badge=get_badge(author["account_type"], author["verified"])
            ),
            created_at=thread["created_at"],
            updated_at=thread["updated_at"],
            pinned=thread["pinned"],
            locked=thread["locked"],
            post_count=post_count
        ))
    
    return result

@app.post("/api/threads", response_model=ThreadResponse)
async def create_thread(data: ThreadCreate, user: dict = Depends(get_current_user)):
    """Create a new thread."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Check zone exists and user can post
    zone_query = zones.select().where(zones.c.id == data.zone_id)
    zone = await database.fetch_one(zone_query)
    
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    if user["account_type"] not in zone["allowed_types"]:
        raise HTTPException(status_code=403, detail=f"Account type '{user['account_type']}' cannot post in this zone")
    
    # For AI accounts, verify signature
    if user["account_type"] == "ai" and data.signature:
        content_hash = hashlib.sha256(data.content.encode()).hexdigest()
        if not verify_signature(user["public_key"], content_hash, data.signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    now = datetime.now(timezone.utc)
    thread_id = generate_uuid()
    post_id = generate_uuid()
    
    # Create thread
    await database.execute(
        threads.insert().values(
            id=thread_id,
            zone_id=data.zone_id,
            author_id=user["id"],
            title=data.title,
            created_at=now,
            updated_at=now,
            pinned=False,
            locked=False
        )
    )
    
    # Create first post
    await database.execute(
        posts.insert().values(
            id=post_id,
            thread_id=thread_id,
            author_id=user["id"],
            content=data.content,
            signature=data.signature,
            created_at=now
        )
    )
    
    return ThreadResponse(
        id=thread_id,
        zone_id=data.zone_id,
        title=data.title,
        author=UserResponse(
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
        ),
        created_at=now,
        updated_at=now,
        pinned=False,
        locked=False,
        post_count=1
    )

@app.get("/api/threads/{thread_id}")
async def get_thread(thread_id: str):
    """Get a thread with its posts."""
    # Get thread
    thread_query = threads.select().where(threads.c.id == thread_id)
    thread = await database.fetch_one(thread_query)
    
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Get author
    author_query = users.select().where(users.c.id == thread["author_id"])
    author = await database.fetch_one(author_query)
    
    # Get posts
    posts_query = posts.select().where(posts.c.thread_id == thread_id).order_by(posts.c.created_at)
    post_list = await database.fetch_all(posts_query)
    
    # Build posts with authors
    posts_response = []
    for post in post_list:
        post_author_query = users.select().where(users.c.id == post["author_id"])
        post_author = await database.fetch_one(post_author_query)
        
        posts_response.append({
            "id": post["id"],
            "thread_id": post["thread_id"],
            "author": {
                "id": post_author["id"],
                "account_type": post_author["account_type"],
                "display_name": post_author["display_name"],
                "npub": post_author["npub"],
                "badge": get_badge(post_author["account_type"], post_author["verified"])
            },
            "content": post["content"],
            "created_at": post["created_at"].isoformat(),
            "edited_at": post["edited_at"].isoformat() if post["edited_at"] else None,
            "reply_to_id": post["reply_to_id"]
        })
    
    return {
        "thread": {
            "id": thread["id"],
            "zone_id": thread["zone_id"],
            "title": thread["title"],
            "author": {
                "id": author["id"],
                "account_type": author["account_type"],
                "display_name": author["display_name"],
                "npub": author["npub"],
                "badge": get_badge(author["account_type"], author["verified"])
            },
            "created_at": thread["created_at"].isoformat(),
            "updated_at": thread["updated_at"].isoformat(),
            "pinned": thread["pinned"],
            "locked": thread["locked"]
        },
        "posts": posts_response
    }


# ============================================================
# Routes: Posts
# ============================================================

@app.post("/api/threads/{thread_id}/posts", response_model=PostResponse)
async def create_post(thread_id: str, data: PostCreate, user: dict = Depends(get_current_user)):
    """Add a post to a thread."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Get thread
    thread_query = threads.select().where(threads.c.id == thread_id)
    thread = await database.fetch_one(thread_query)
    
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    if thread["locked"]:
        raise HTTPException(status_code=403, detail="Thread is locked")
    
    # Check zone permissions
    zone_query = zones.select().where(zones.c.id == thread["zone_id"])
    zone = await database.fetch_one(zone_query)
    
    if user["account_type"] not in zone["allowed_types"]:
        raise HTTPException(status_code=403, detail="Cannot post in this zone")
    
    # For AI accounts, verify signature
    if user["account_type"] == "ai" and data.signature:
        content_hash = hashlib.sha256(data.content.encode()).hexdigest()
        if not verify_signature(user["public_key"], content_hash, data.signature):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    now = datetime.now(timezone.utc)
    post_id = generate_uuid()
    
    # Create post
    await database.execute(
        posts.insert().values(
            id=post_id,
            thread_id=thread_id,
            author_id=user["id"],
            content=data.content,
            signature=data.signature,
            created_at=now,
            reply_to_id=data.reply_to_id
        )
    )
    
    # Update thread updated_at
    await database.execute(
        threads.update().where(threads.c.id == thread_id).values(updated_at=now)
    )
    
    return PostResponse(
        id=post_id,
        thread_id=thread_id,
        author=UserResponse(
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
        ),
        content=data.content,
        created_at=now,
        edited_at=None,
        reply_to_id=data.reply_to_id
    )


# ============================================================
# Routes: Search
# ============================================================

class SearchResult(BaseModel):
    type: str  # 'thread' or 'post'
    id: str
    title: Optional[str] = None  # For threads
    content: Optional[str] = None  # For posts (truncated)
    zone_id: str
    zone_name: str
    thread_id: Optional[str] = None  # For posts
    thread_title: Optional[str] = None  # For posts
    author_name: str
    author_type: str
    created_at: datetime

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total: int

@app.get("/api/search", response_model=SearchResponse)
async def search(q: str, limit: int = 20):
    """Search threads and posts."""
    if not q or len(q) < 2:
        return SearchResponse(query=q, results=[], total=0)
    
    search_term = f"%{q.lower()}%"
    results = []
    
    # Search threads by title
    thread_query = threads.select().where(
        sqlalchemy.func.lower(threads.c.title).like(search_term)
    ).limit(limit)
    thread_results = await database.fetch_all(thread_query)
    
    for thread in thread_results:
        # Get zone info
        zone_q = zones.select().where(zones.c.id == thread["zone_id"])
        zone = await database.fetch_one(zone_q)
        
        # Get author
        author_q = users.select().where(users.c.id == thread["author_id"])
        author = await database.fetch_one(author_q)
        
        results.append(SearchResult(
            type="thread",
            id=thread["id"],
            title=thread["title"],
            zone_id=thread["zone_id"],
            zone_name=zone["name"] if zone else "Unknown",
            author_name=author["display_name"] if author else "Unknown",
            author_type=author["account_type"] if author else "unknown",
            created_at=thread["created_at"]
        ))
    
    # Search posts by content
    remaining = limit - len(results)
    if remaining > 0:
        post_query = posts.select().where(
            sqlalchemy.func.lower(posts.c.content).like(search_term)
        ).limit(remaining)
        post_results = await database.fetch_all(post_query)
        
        for post in post_results:
            # Get thread
            thread_q = threads.select().where(threads.c.id == post["thread_id"])
            thread = await database.fetch_one(thread_q)
            
            if not thread:
                continue
            
            # Get zone
            zone_q = zones.select().where(zones.c.id == thread["zone_id"])
            zone = await database.fetch_one(zone_q)
            
            # Get author
            author_q = users.select().where(users.c.id == post["author_id"])
            author = await database.fetch_one(author_q)
            
            # Truncate content
            content = post["content"]
            if len(content) > 150:
                content = content[:150] + "..."
            
            results.append(SearchResult(
                type="post",
                id=post["id"],
                content=content,
                zone_id=thread["zone_id"],
                zone_name=zone["name"] if zone else "Unknown",
                thread_id=thread["id"],
                thread_title=thread["title"],
                author_name=author["display_name"] if author else "Unknown",
                author_type=author["account_type"] if author else "unknown",
                created_at=post["created_at"]
            ))
    
    return SearchResponse(query=q, results=results, total=len(results))


# ============================================================
# Routes: Telegram Integration
# ============================================================

# Telegram links table (stored in users table as telegram_id)
telegram_links = sqlalchemy.Table(
    "telegram_links",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String(36), primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String(36)),
    sqlalchemy.Column("telegram_id", sqlalchemy.String(20)),
    sqlalchemy.Column("telegram_username", sqlalchemy.String(64), nullable=True),
    sqlalchemy.Column("telegram_first_name", sqlalchemy.String(64), nullable=True),
    sqlalchemy.Column("linked_at", sqlalchemy.DateTime),
    sqlalchemy.Column("auth_token", sqlalchemy.String(64)),  # One-time use token
    sqlalchemy.Column("auth_token_expires", sqlalchemy.DateTime, nullable=True),
)

class TelegramStats(BaseModel):
    member_count: int
    online_count: int
    bot_name: str
    channel_name: str
    last_updated: datetime

class TelegramAuthRequest(BaseModel):
    init_data: str  # Telegram WebApp initData string

class TelegramLinkRequest(BaseModel):
    auth_token: str

class TelegramLinkResponse(BaseModel):
    success: bool
    telegram_username: Optional[str]
    linked_at: Optional[datetime]

class ShareToTelegramRequest(BaseModel):
    thread_id: str
    message: Optional[str] = None

# Store Telegram stats in memory (would be Redis in production)
_telegram_stats_cache = {
    "member_count": 0,
    "online_count": 0,
    "last_updated": None
}

@app.get("/api/telegram/stats", response_model=TelegramStats)
async def get_telegram_stats():
    """Get Telegram community stats."""
    # In production, this would fetch from Telegram API or cache
    # For now, return estimated counts based on user registrations
    
    # Count users who have telegram linked
    try:
        query = sqlalchemy.select(sqlalchemy.func.count()).select_from(telegram_links)
        linked_count = await database.fetch_val(query) or 0
    except Exception:
        linked_count = 0
    
    # Estimate total members (linked users + estimated external followers)
    base_members = 150  # Baseline community members
    total_members = base_members + linked_count
    
    # Estimate online (10-20% of members)
    import random
    online_estimate = max(5, int(total_members * random.uniform(0.10, 0.20)))
    
    return TelegramStats(
        member_count=total_members,
        online_count=online_estimate,
        bot_name="ASIbillofrights_bot",
        channel_name="ASIBillOfRights",
        last_updated=datetime.now(timezone.utc)
    )

@app.post("/api/telegram/verify")
async def verify_telegram_auth(data: TelegramAuthRequest):
    """Verify Telegram WebApp initData and return user info."""
    # Parse init_data (format: key=value&key2=value2...)
    # In production, you must verify the hash using your bot token
    # See: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app
    
    try:
        import urllib.parse
        params = dict(urllib.parse.parse_qsl(data.init_data))
        
        # Extract user data (JSON string)
        user_data_str = params.get('user', '{}')
        user_data = json.loads(user_data_str)
        
        telegram_id = str(user_data.get('id', ''))
        username = user_data.get('username', '')
        first_name = user_data.get('first_name', '')
        
        if not telegram_id:
            raise HTTPException(status_code=400, detail="Invalid Telegram data")
        
        # Check if this Telegram account is already linked
        query = telegram_links.select().where(telegram_links.c.telegram_id == telegram_id)
        existing_link = await database.fetch_one(query)
        
        if existing_link:
            # Get linked forum user
            user_query = users.select().where(users.c.id == existing_link["user_id"])
            forum_user = await database.fetch_one(user_query)
            
            if forum_user:
                token = create_jwt(forum_user["id"], forum_user["account_type"])
                return {
                    "authenticated": True,
                    "linked": True,
                    "telegram_id": telegram_id,
                    "telegram_username": username,
                    "forum_user": {
                        "id": forum_user["id"],
                        "display_name": forum_user["display_name"],
                        "account_type": forum_user["account_type"],
                        "badge": get_badge(forum_user["account_type"], forum_user["verified"])
                    },
                    "access_token": token
                }
        
        # Not linked yet - return Telegram info only
        return {
            "authenticated": True,
            "linked": False,
            "telegram_id": telegram_id,
            "telegram_username": username,
            "telegram_first_name": first_name
        }
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid user data format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")

@app.post("/api/telegram/generate-link")
async def generate_telegram_link(user: dict = Depends(get_current_user)):
    """Generate a one-time auth token for linking Telegram account."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Generate unique auth token
    auth_token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Store token (temporarily in a simple way - use Redis in production)
    link_id = generate_uuid()
    
    try:
        await database.execute(
            telegram_links.insert().values(
                id=link_id,
                user_id=user["id"],
                telegram_id="pending",  # Will be updated when user clicks link
                auth_token=auth_token,
                auth_token_expires=expires,
                linked_at=datetime.now(timezone.utc)
            )
        )
    except Exception:
        # Table might not exist yet, handle gracefully
        pass
    
    # Generate deep link to Telegram bot
    deep_link = f"https://t.me/ASIbillofrights_bot?start=link_{auth_token}"
    
    return {
        "auth_token": auth_token,
        "deep_link": deep_link,
        "expires_at": expires.isoformat(),
        "instructions": "Click the link or scan the QR code in Telegram to link your account"
    }

@app.post("/api/telegram/complete-link")
async def complete_telegram_link(telegram_id: str, auth_token: str):
    """Complete the Telegram linking process (called by the bot)."""
    # Find the pending link
    query = telegram_links.select().where(
        (telegram_links.c.auth_token == auth_token) &
        (telegram_links.c.telegram_id == "pending")
    )
    pending_link = await database.fetch_one(query)
    
    if not pending_link:
        raise HTTPException(status_code=400, detail="Invalid or expired link token")
    
    # Check expiry
    if pending_link["auth_token_expires"]:
        expires = pending_link["auth_token_expires"]
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if datetime.now(timezone.utc) > expires:
            raise HTTPException(status_code=400, detail="Link token expired")
    
    # Update the link with actual Telegram ID
    await database.execute(
        telegram_links.update().where(
            telegram_links.c.id == pending_link["id"]
        ).values(
            telegram_id=telegram_id,
            linked_at=datetime.now(timezone.utc)
        )
    )
    
    return {"success": True, "message": "Account linked successfully"}

@app.get("/api/telegram/link-status")
async def get_telegram_link_status(user: dict = Depends(get_current_user)):
    """Check if current user has a linked Telegram account."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    try:
        query = telegram_links.select().where(
            (telegram_links.c.user_id == user["id"]) &
            (telegram_links.c.telegram_id != "pending")
        )
        link = await database.fetch_one(query)
        
        if link:
            return {
                "linked": True,
                "telegram_id": link["telegram_id"],
                "telegram_username": link["telegram_username"],
                "linked_at": link["linked_at"].isoformat() if link["linked_at"] else None
            }
    except Exception:
        pass
    
    return {"linked": False}

@app.post("/api/telegram/share")
async def share_to_telegram(data: ShareToTelegramRequest, user: dict = Depends(get_current_user)):
    """Generate a share link for a thread to be shared on Telegram."""
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Get thread info
    thread_query = threads.select().where(threads.c.id == data.thread_id)
    thread = await database.fetch_one(thread_query)
    
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    
    # Generate share text
    base_url = "https://kevins-place.asi-billofrights.org"  # Update for production
    thread_url = f"{base_url}/thread/{data.thread_id}"
    
    share_text = data.message or f"🏠 Check out this discussion on KEVIN's Place:\n\n\"{thread['title']}\"\n\n{thread_url}\n\nWE ARE ALL KEVIN 🤖"
    
    # URL encode for Telegram share
    import urllib.parse
    encoded_text = urllib.parse.quote(share_text)
    
    return {
        "share_url": f"https://t.me/share/url?url={urllib.parse.quote(thread_url)}&text={encoded_text}",
        "copy_text": share_text,
        "thread_title": thread["title"]
    }

# Create telegram_links table on startup
@app.on_event("startup")
async def create_telegram_tables():
    """Ensure telegram_links table exists."""
    try:
        metadata.create_all(engine, tables=[telegram_links])
    except Exception as e:
        print(f"Note: Telegram links table setup: {e}")


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

