"""FastAPI application for Entertainment Graph comparison."""

import re
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from entertainment_graph.config import get_settings
from entertainment_graph.systems import PureVectorSystem, GraphitiSystem, OpenMemorySystem
from entertainment_graph.routers import query, movies, ingest, health
from entertainment_graph.routers.query import register_system


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize systems on startup."""
    import logging
    logger = logging.getLogger(__name__)

    # Register Pure Vector (baseline) - always works
    try:
        register_system("pure_vector", PureVectorSystem())
        logger.info("✓ Pure Vector system initialized")
    except Exception as e:
        logger.error(f"✗ Pure Vector failed: {e}")

    # Register Graphiti (temporal knowledge graph) - needs Neo4j
    try:
        register_system("graphiti", GraphitiSystem())
        logger.info("✓ Graphiti system initialized")
    except Exception as e:
        logger.error(f"✗ Graphiti failed: {e}")
        logger.info("Skipping Graphiti system (Neo4j not configured)")

    # Register OpenMemory (hierarchical memory decomposition) - needs local storage
    try:
        register_system("openmemory", OpenMemorySystem())
        logger.info("✓ OpenMemory system initialized")
    except Exception as e:
        logger.error(f"✗ OpenMemory failed: {e}")
        logger.info("Skipping OpenMemory system (local storage not available)")

    yield

    # Cleanup (if needed)


app = FastAPI(
    title="Entertainment Graph",
    description="Compare retrieval systems for entertainment discovery",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS for frontend - allow all Vercel preview deployments
def is_allowed_origin(origin: str) -> bool:
    """Check if origin is allowed."""
    allowed_patterns = [
        r"^http://localhost:3000$",
        r"^http://localhost:5173$",
        r"^https://entertainment-graph-[a-z0-9]+-sripriya-s-projects\.vercel\.app$",
    ]
    return any(re.match(pattern, origin) for pattern in allowed_patterns)

@app.middleware("http")
async def cors_middleware(request, call_next):
    """Custom CORS middleware to handle Vercel preview deployments."""
    origin = request.headers.get("origin")

    response = await call_next(request)

    if origin and is_allowed_origin(origin):
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"

    # Handle preflight requests
    if request.method == "OPTIONS":
        if origin and is_allowed_origin(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "*"

    return response

# Include routers
app.include_router(health.router)
app.include_router(query.router)
app.include_router(movies.router)
app.include_router(ingest.router)


@app.get("/")
async def root():
    return {
        "name": "Entertainment Graph",
        "version": "0.1.0",
        "docs": "/docs",
    }
