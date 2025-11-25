"""Test Graphiti system with sample movie data."""

import asyncio
import json
from pathlib import Path

from entertainment_graph.models import Movie
from entertainment_graph.systems import GraphitiSystem


async def main():
    print("=== Testing Graphiti System ===\n")

    # 1. Initialize system
    print("1. Initializing Graphiti system...")
    system = GraphitiSystem()
    print(f"   System name: {system.name}")

    # 2. Health check
    print("\n2. Checking system health...")
    try:
        is_healthy = await system.health_check()
        print(f"   Health check: {'✓ PASS' if is_healthy else '✗ FAIL'}")
    except Exception as e:
        print(f"   Health check failed: {e}")
        print("   Make sure Neo4j is running and credentials are correct in .env")
        return

    # 3. Load sample movies
    print("\n3. Loading sample movies...")
    data_dir = Path(__file__).parent.parent / "data" / "movies"
    movies = []

    for movie_file in data_dir.glob("*.json"):
        with open(movie_file) as f:
            movie_data = json.load(f)
            movies.append(Movie(**movie_data))
            print(f"   Loaded: {movie_data['title']}")

    if not movies:
        print("   No movies found! Check data/movies/ directory")
        return

    # 4. Ingest movies
    print(f"\n4. Ingesting {len(movies)} movies into Graphiti...")
    try:
        count = await system.ingest(movies)
        print(f"   ✓ Ingested {count} movies")
        print("   Graphiti extracted entities and relationships from movie descriptions")
    except Exception as e:
        print(f"   ✗ Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        return

    # 5. Test queries
    print("\n5. Testing queries...\n")

    test_queries = [
        "Movies with dystopian corporate themes",
        "Films similar to Blade Runner's visual style",
        "Denis Villeneuve movies",
    ]

    for query in test_queries:
        print(f"Query: \"{query}\"")
        try:
            response = await system.query(query, limit=3)
            print(f"Reasoning: {response.reasoning}")
            print("Results:")
            for i, result in enumerate(response.results, 1):
                print(f"  {i}. {result.title} ({result.year}) - Score: {result.score:.2f}")
                print(f"     {result.explanation}")
                if result.retrieval_context:
                    graph_info = result.retrieval_context
                    if graph_info.get("graph_nodes"):
                        print(f"     Graph nodes: {graph_info['graph_nodes'][:3]}")
            print()
        except Exception as e:
            print(f"  ✗ Query failed: {e}")
            import traceback
            traceback.print_exc()
            print()

    print("=== Test Complete ===")


if __name__ == "__main__":
    asyncio.run(main())
