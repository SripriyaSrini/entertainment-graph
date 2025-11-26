"""FastAPI application for Entertainment Graph comparison."""

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

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
