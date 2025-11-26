#!/usr/bin/env python3
"""Ingest movies to Graphiti system (with longer timeout for graph processing)."""

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

if __name__ == "__main__":
    print("\n🚀 Ingesting Movies to Graphiti System\n")
    print("Note: Graphiti builds a knowledge graph, which takes longer.\n")

    # Load all movies
    print("Loading movies from data/movies/...")
    movies = load_all_movies()

    if not movies:
        print("\n❌ No movies found in data/movies/ directory")
        exit(1)

    print(f"\n✓ Loaded {len(movies)} movies total\n")

    # Ingest to Graphiti with longer timeout (2 minutes)
    print("="*70)
    print(f"Ingesting {len(movies)} movies to Graphiti (this may take 1-2 minutes)...")
    print("="*70)

    payload = {"movies": movies}

    try:
        response = requests.post(
            f"{API_URL}/ingest/graphiti/bulk",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=120  # 2 minute timeout for Graphiti
        )

        print(f"\nStatus: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")

        if response.status_code == 200:
            count = result.get("movies_ingested", 0)
            if count > 0:
                print(f"\n✅ Successfully ingested {count} movies to Graphiti!")
            else:
                print(f"\n⚠️  No movies were ingested")
        else:
            print(f"\n❌ Error {response.status_code}")

    except requests.exceptions.Timeout:
        print("\n⚠️  Request timed out after 2 minutes.")
        print("Graphiti graph processing may still be running on the server.")
        print("Check the Railway logs or try querying Graphiti to see if it worked.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

    print("\n" + "="*70)
    print("✅ Done!")
    print("="*70)
