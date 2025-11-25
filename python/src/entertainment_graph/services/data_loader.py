"""Load movie data from JSON files."""

import json
from pathlib import Path

from entertainment_graph.models import Movie


def load_movies(data_dir: str = "data/movies") -> list[Movie]:
    """Load all movies from JSON files in the data directory."""
    movies = []
    data_path = Path(data_dir)

    if not data_path.exists():
        return movies

    for file_path in data_path.glob("*.json"):
        with open(file_path) as f:
            data = json.load(f)
            movies.append(Movie(**data))

    return movies


def load_movie(movie_id: str, data_dir: str = "data/movies") -> Movie | None:
    """Load a single movie by ID."""
    file_path = Path(data_dir) / f"{movie_id}.json"

    if not file_path.exists():
        return None

    with open(file_path) as f:
        data = json.load(f)
        return Movie(**data)
