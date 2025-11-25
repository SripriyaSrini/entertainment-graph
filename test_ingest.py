#!/usr/bin/env python3
"""Test the /ingest endpoint with sample movie data."""

import requests
import json

API_URL = "https://web-production-b84b0.up.railway.app"

# Sample movie data (simplified from dune-2021.json)
dune_movie = {
    "id": "dune-2021",
    "title": "Dune",
    "year": 2021,
    "runtime_minutes": 155,
    "genres": ["Science Fiction", "Adventure", "Drama"],
    "director": ["Denis Villeneuve"],
    "cast": ["Timothée Chalamet", "Rebecca Ferguson", "Oscar Isaac", "Josh Brolin"],
    "plot_summary": "Paul Atreides, a brilliant young man born into a great destiny, must travel to the most dangerous planet in the universe to ensure the future of his family and his people.",
    "themes": [
        {
            "name": "Destiny and prophecy",
            "specificity": "Chosen one narrative",
            "prominence": "central"
        },
        {
            "name": "Power and politics",
            "specificity": "Imperial control and resource wars",
            "prominence": "central"
        }
    ],
    "mood": {
        "primary": ["Epic", "Contemplative", "Mystical"],
        "undertones": ["Foreboding", "Reverent"],
        "intensity": "intense",
        "emotional_arc": "Growing from wonder to determination"
    },
    "visual_style": {
        "palette": ["Desert ochre", "Deep shadows", "Metallic grays"],
        "composition": ["Vast landscapes", "Monumental architecture"],
        "descriptors": ["Cinematic", "Immersive", "Grand scale"]
    },
    "narrative": {
        "pacing": "Slow-burn, deliberate",
        "structure": "Hero's journey, world-building focused",
        "tone": "Serious, philosophical",
        "perspective": "Third-person ensemble"
    }
}

her_movie = {
    "id": "her-2013",
    "title": "Her",
    "year": 2013,
    "runtime_minutes": 126,
    "genres": ["Science Fiction", "Romance", "Drama"],
    "director": ["Spike Jonze"],
    "cast": ["Joaquin Phoenix", "Scarlett Johansson", "Amy Adams"],
    "plot_summary": "In a near future, a lonely writer develops an unlikely relationship with an operating system designed to meet his every need.",
    "themes": [
        {
            "name": "Love and connection",
            "specificity": "Human-AI relationships",
            "prominence": "central"
        },
        {
            "name": "Loneliness and isolation",
            "specificity": "Urban alienation",
            "prominence": "central"
        }
    ],
    "mood": {
        "primary": ["Melancholic", "Intimate", "Wistful"],
        "undertones": ["Hopeful", "Bittersweet"],
        "intensity": "moderate",
        "emotional_arc": "Loneliness to connection to acceptance"
    },
    "visual_style": {
        "palette": ["Warm pastels", "Soft lighting", "Pastel tones"],
        "composition": ["Clean lines", "Minimalist interiors"],
        "descriptors": ["Dreamlike", "Intimate", "Pastel aesthetic"]
    },
    "narrative": {
        "pacing": "Contemplative, unhurried",
        "structure": "Character-driven, linear",
        "tone": "Gentle, introspective",
        "perspective": "Third-person focused on Theodore"
    }
}

def test_ingest_bulk():
    """Test the new /ingest/bulk endpoint."""
    print("=" * 70)
    print("Testing /ingest/{system_name}/bulk endpoint")
    print("=" * 70)
    print()

    # Test ingesting to Pure Vector system
    payload = {
        "movies": [dune_movie, her_movie]
    }

    print(f"Ingesting {len(payload['movies'])} movies to Pure Vector system...")
    response = requests.post(
        f"{API_URL}/ingest/pure_vector/bulk",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

    if response.status_code == 200:
        result = response.json()
        if result.get("movies_ingested", 0) > 0:
            print("✅ Movies successfully ingested!")
            return True
        else:
            print("⚠️  No movies were ingested")
            return False
    else:
        print(f"❌ Error: {response.status_code}")
        return False

def test_query_after_ingest():
    """Test querying after ingesting data."""
    print("=" * 70)
    print("Testing query after ingestion")
    print("=" * 70)
    print()

    queries = [
        "epic science fiction with desert landscapes",
        "intimate love story about technology",
        "Denis Villeneuve movies"
    ]

    for query in queries:
        print(f"Query: '{query}'")
        response = requests.post(
            f"{API_URL}/query/pure_vector",
            json={"query": query, "limit": 3},
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            result = response.json()
            results = result.get("results", [])
            print(f"  Found {len(results)} results:")
            for movie in results:
                print(f"    - {movie.get('title')} ({movie.get('year')})")
        else:
            print(f"  Error: {response.status_code}")
        print()

if __name__ == "__main__":
    print("\n🚀 Testing Entertainment Graph Ingest Endpoint\n")

    try:
        # Test ingestion
        success = test_ingest_bulk()

        if success:
            # Test queries
            test_query_after_ingest()

        print("=" * 70)
        print("✅ Test completed!")
        print("=" * 70)
        print(f"\nAPI Documentation: {API_URL}/docs")
        print("Try the interactive docs to test more endpoints!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        print("\nMake sure the Railway deployment is running!")
