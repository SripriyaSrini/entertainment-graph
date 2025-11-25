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
    # Register Pure Vector (baseline)
    register_system("pure_vector", PureVectorSystem())

    # Register Graphiti (temporal knowledge graph)
    register_system("graphiti", GraphitiSystem())

    # Register OpenMemory (hierarchical memory decomposition)
    register_system("openmemory", OpenMemorySystem())

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
