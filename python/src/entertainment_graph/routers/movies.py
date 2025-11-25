"""Movie data endpoints."""

from fastapi import APIRouter, HTTPException

from entertainment_graph.models import Movie
from entertainment_graph.services.data_loader import load_movies, load_movie

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("", response_model=list[Movie])
async def list_movies() -> list[Movie]:
    """List all movies in the dataset."""
    return load_movies()


@router.get("/{movie_id}", response_model=Movie)
async def get_movie(movie_id: str) -> Movie:
    """Get a specific movie by ID."""
    movie = load_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail=f"Movie '{movie_id}' not found")
    return movie
