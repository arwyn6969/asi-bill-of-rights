"""
KEVIN's Place - Backend API

A forum for all minds: Human, AI, and Hybrid.
Built with FastAPI for the ASI Bill of Rights project.

This is the main application factory with router assembly.
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import APP_NAME, APP_DESCRIPTION, APP_VERSION, CORS_ORIGINS
from database import database, metadata, engine, zones


# ============================================================
# Application Lifespan
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    metadata.create_all(engine)
    await database.connect()
    await seed_zones()
    yield
    # Shutdown
    await database.disconnect()


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
# Application Factory
# ============================================================

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=APP_NAME,
        description=APP_DESCRIPTION,
        version=APP_VERSION,
        lifespan=lifespan
    )
    
    # CORS middleware
    origins = CORS_ORIGINS if CORS_ORIGINS != ["*"] else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    from routers import (
        auth_router,
        zones_router,
        threads_router,
        posts_router,
        search_router,
        telegram_router,
    )
    
    app.include_router(auth_router)
    app.include_router(zones_router)
    app.include_router(threads_router)
    app.include_router(posts_router)
    app.include_router(search_router)
    app.include_router(telegram_router)
    
    # Health and info routes
    @app.get("/")
    async def root():
        """API root - welcome message."""
        return {
            "name": APP_NAME,
            "version": APP_VERSION,
            "message": "A forum for all minds. WE ARE ALL KEVIN. 🤖",
            "docs": "/docs",
            "zones": "/api/zones"
        }

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}
    
    return app


# Create the application instance
app = create_app()
