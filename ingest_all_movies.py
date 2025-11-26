#!/usr/bin/env python3
"""Ingest all movies from data/movies directory to Railway deployment."""

import requests
import json
from pathlib import Path

API_URL = "https://web-production-b84b0.up.railway.app"

def load_all_movies():
    """Load all movies from local data/movies directory."""
    movies = []
    data_path = Path("data/movies")

    if not data_path.exists():
        print(f"❌ Directory {data_path} not found")
        return movies

    for file_path in data_path.glob("*.json"):
        with open(file_path) as f:
            movie = json.load(f)
            movies.append(movie)
            print(f"  ✓ Loaded {movie.get('title')} ({movie.get('year')})")

    return movies

def ingest_to_system(system_name: str, movies: list):
    """Ingest all movies to a specific system."""
    print(f"\n{'='*70}")
    print(f"Ingesting {len(movies)} movies to {system_name}")
    print(f"{'='*70}")

    payload = {"movies": movies}

    try:
        response = requests.post(
            f"{API_URL}/ingest/{system_name}/bulk",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        if response.status_code == 200:
            count = result.get("movies_ingested", 0)
            if count > 0:
                print(f"✅ Successfully ingested {count} movies to {system_name}!")
                return True
            else:
                print(f"⚠️  No movies were ingested to {system_name}")
                return False
        else:
            print(f"❌ Error {response.status_code}: {result}")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_query(system_name: str, query: str):
    """Test a query on a system."""
    response = requests.post(
        f"{API_URL}/query/{system_name}",
        json={"query": query, "limit": 3},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code == 200:
        result = response.json()
        results = result.get("results", [])
        print(f"\n  Query: '{query}'")
        print(f"  Found {len(results)} results:")
        for movie in results:
            print(f"    - {movie.get('title')} ({movie.get('year')})")
    else:
        print(f"  Error: {response.status_code}")

if __name__ == "__main__":
    print("\n🚀 Ingesting All Movies to Railway Deployment\n")

    # Load all movies from local directory
    print("Loading movies from data/movies/...")
    movies = load_all_movies()

    if not movies:
        print("\n❌ No movies found in data/movies/ directory")
        exit(1)

    print(f"\n✓ Loaded {len(movies)} movies total\n")

    # Ingest to Pure Vector system
    success = ingest_to_system("pure_vector", movies)

    if success:
        # Ingest to Graphiti system too (if available)
        print("\n" + "="*70)
        print("Also ingesting to Graphiti system...")
        print("="*70)
        ingest_to_system("graphiti", movies)

        # Test some queries
        print("\n" + "="*70)
        print("Testing Queries")
        print("="*70)

        test_query("pure_vector", "epic science fiction with desert landscapes")
        test_query("pure_vector", "intimate stories about technology and loneliness")
        test_query("pure_vector", "Denis Villeneuve movies")

    print("\n" + "="*70)
    print("✅ Done!")
    print("="*70)
    print(f"\nView API docs: {API_URL}/docs")
