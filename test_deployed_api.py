#!/usr/bin/env python3
"""Test the deployed Railway API."""

import requests
import json

# Your Railway URL
API_URL = "https://web-production-b84b0.up.railway.app"

def test_health():
    """Test the health endpoint."""
    print("=" * 60)
    print("TEST 1: Health Check")
    print("=" * 60)

    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_root():
    """Test the root endpoint."""
    print("=" * 60)
    print("TEST 2: Root Endpoint")
    print("=" * 60)

    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_query_pure_vector():
    """Test query with Pure Vector system (no data yet)."""
    print("=" * 60)
    print("TEST 3: Query Pure Vector (empty - no movies ingested yet)")
    print("=" * 60)

    payload = {
        "query": "science fiction movies",
        "system": "pure_vector",
        "limit": 5
    }

    response = requests.post(f"{API_URL}/query", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_query_graphiti():
    """Test query with Graphiti system (no data yet)."""
    print("=" * 60)
    print("TEST 4: Query Graphiti (empty - no movies ingested yet)")
    print("=" * 60)

    payload = {
        "query": "Denis Villeneuve movies",
        "system": "graphiti",
        "limit": 5
    }

    response = requests.post(f"{API_URL}/query", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_ingest_movie():
    """Test ingesting a movie."""
    print("=" * 60)
    print("TEST 5: Ingest a Movie")
    print("=" * 60)

    movie_data = {
        "id": "dune_2021",
        "title": "Dune",
        "year": 2021,
        "director": "Denis Villeneuve",
        "plot": "A noble family becomes embroiled in a war for control of the galaxy's most valuable asset.",
        "themes": ["power", "destiny", "ecology", "colonialism"],
        "mood": "epic, contemplative, visually stunning",
        "visual_style": "vast desert landscapes, monumental architecture, muted earth tones",
        "narrative": "Hero's journey, slow-burn world-building"
    }

    payload = {
        "movies": [movie_data],
        "system": "pure_vector"
    }

    response = requests.post(f"{API_URL}/ingest", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_query_after_ingest():
    """Test query after ingesting data."""
    print("=" * 60)
    print("TEST 6: Query After Ingesting Dune")
    print("=" * 60)

    payload = {
        "query": "epic science fiction with desert landscapes",
        "system": "pure_vector",
        "limit": 3
    }

    response = requests.post(f"{API_URL}/query", json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Found {len(result.get('results', []))} movies")
    print(f"Response: {json.dumps(result, indent=2)}")
    print()

if __name__ == "__main__":
    print("\n🚀 Testing Entertainment Graph API on Railway\n")

    try:
        # Basic tests
        test_health()
        test_root()

        # Query tests (will be empty initially)
        test_query_pure_vector()
        test_query_graphiti()

        # Ingest and query
        test_ingest_movie()
        test_query_after_ingest()

        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print(f"\nAPI Documentation: {API_URL}/docs")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        print("\nMake sure the Railway deployment is running!")
