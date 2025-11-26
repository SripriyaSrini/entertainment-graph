#!/usr/bin/env python3
"""Test what's in the Graphiti system."""

import requests
import json

API_URL = "https://web-production-b84b0.up.railway.app"

def test_graphiti_query(query: str, limit: int = 5):
    """Test a query on Graphiti system."""
    print(f"\nQuery: '{query}'")
    print("-" * 70)

    try:
        response = requests.post(
            f"{API_URL}/query/graphiti",
            json={"query": query, "limit": limit},
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            results = result.get("results", [])
            reasoning = result.get("reasoning", "")

            print(f"Status: {response.status_code}")
            print(f"Found {len(results)} results")

            if reasoning:
                print(f"\nReasoning: {reasoning}")

            if results:
                print("\nResults:")
                for i, movie in enumerate(results, 1):
                    print(f"  {i}. {movie.get('title')} ({movie.get('year')})")
                    if 'director' in movie:
                        print(f"     Director: {', '.join(movie['director'])}")
                    if 'score' in movie:
                        print(f"     Score: {movie['score']:.3f}")
            else:
                print("\n⚠️  No results found (database may be empty)")

        elif response.status_code == 404:
            print(f"❌ Error 404: Graphiti system not found")
            print("The system may not be initialized on Railway")
        else:
            print(f"❌ Error {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.Timeout:
        print("⚠️  Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Testing Graphiti System")
    print("="*70)

    # Test multiple queries to see what's in Graphiti
    test_queries = [
        "Denis Villeneuve movies",
        "science fiction films",
        "movies about artificial intelligence",
        "psychological thrillers",
        "all movies"  # Generic query to see everything
    ]

    for query in test_queries:
        test_graphiti_query(query, limit=5)

    print("\n" + "="*70)
    print("✅ Done!")
    print("="*70)
    print(f"\nView API docs: {API_URL}/docs")
