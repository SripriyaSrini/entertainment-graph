"""Ingestion endpoints."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from entertainment_graph.models.movie import Movie
from entertainment_graph.services.data_loader import load_movies
from entertainment_graph.routers.query import get_systems

router = APIRouter(prefix="/ingest", tags=["ingest"])


class IngestResponse(BaseModel):
    system: str
    movies_ingested: int


class IngestAllResponse(BaseModel):
    results: list[IngestResponse]


class IngestRequest(BaseModel):
    """Request to ingest movies with data in the body."""
    movies: list[Movie]


@router.post("/{system_name}", response_model=IngestResponse)
async def ingest_to_system(system_name: str) -> IngestResponse:
    """Ingest all movies from data directory into a specific system."""
    systems = get_systems()
    if system_name not in systems:
        return IngestResponse(system=system_name, movies_ingested=-1)

    movies = load_movies()
    system = systems[system_name]
    count = await system.ingest(movies)

    return IngestResponse(system=system_name, movies_ingested=count)


@router.post("/{system_name}/bulk", response_model=IngestResponse)
async def ingest_bulk_to_system(system_name: str, request: IngestRequest) -> IngestResponse:
    """Ingest movies provided in request body into a specific system."""
    systems = get_systems()
    if system_name not in systems:
        raise HTTPException(
            status_code=404,
            detail=f"System '{system_name}' not found. Available: {list(systems.keys())}",
        )

    system = systems[system_name]
    count = await system.ingest(request.movies)

    return IngestResponse(system=system_name, movies_ingested=count)


@router.post("", response_model=IngestAllResponse)
async def ingest_to_all() -> IngestAllResponse:
    """Ingest all movies from data directory into all systems."""
    movies = load_movies()
    results = []

    for name, system in get_systems().items():
        try:
            count = await system.ingest(movies)
            results.append(IngestResponse(system=name, movies_ingested=count))
        except Exception as e:
            results.append(IngestResponse(system=f"{name} (error: {e})", movies_ingested=-1))

    return IngestAllResponse(results=results)
