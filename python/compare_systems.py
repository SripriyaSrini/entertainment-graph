"""Compare Pure Vector vs Graphiti systems side-by-side."""

import asyncio
import json
from pathlib import Path

from entertainment_graph.models import Movie
from entertainment_graph.systems import PureVectorSystem, GraphitiSystem, OpenMemorySystem


async def main():
    print("=== System Comparison: Pure Vector vs Graphiti vs OpenMemory ===\n")

    # Load sample movies
    print("Loading sample movies...")
    data_dir = Path(__file__).parent.parent / "data" / "movies"
    movies = []
    for movie_file in data_dir.glob("*.json"):
        with open(movie_file) as f:
            movie_data = json.load(f)
            movies.append(Movie(**movie_data))
    print(f"Loaded {len(movies)} movies\n")

    # Initialize all three systems
    print("Initializing systems...")
    pure_vector = PureVectorSystem()
    graphiti = GraphitiSystem()
    openmemory = OpenMemorySystem()
    print("✓ All three systems initialized\n")

    # Ingest movies into all systems
    print("Ingesting movies into all systems...")
    print("  Pure Vector: ", end="", flush=True)
    pv_count = await pure_vector.ingest(movies)
    print(f"✓ {pv_count} movies")

    print("  Graphiti: ", end="", flush=True)
    gr_count = await graphiti.ingest(movies)
    print(f"✓ {gr_count} movies")

    print("  OpenMemory: ", end="", flush=True)
    om_count = await openmemory.ingest(movies)
    print(f"✓ {om_count} movies")
    print()

    # Test queries
    test_queries = [
        "Movies with dystopian corporate themes",
        "Films similar to Blade Runner's visual style",
        "Denis Villeneuve movies",
    ]

    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*80}")
        print(f"Query {i}: \"{query}\"")
        print('='*80)

        # Query Pure Vector
        print("\n📊 PURE VECTOR:")
        print("-" * 80)
        pv_response = await pure_vector.query(query, limit=3)
        print(f"Reasoning: {pv_response.reasoning}\n")
        if pv_response.results:
            for j, result in enumerate(pv_response.results, 1):
                print(f"{j}. {result.title} ({result.year}) - Score: {result.score:.3f}")
                print(f"   {result.explanation}")
        else:
            print("No results")

        # Query Graphiti
        print("\n🔗 GRAPHITI:")
        print("-" * 80)
        gr_response = await graphiti.query(query, limit=3)
        print(f"Reasoning: {gr_response.reasoning}\n")
        if gr_response.results:
            for j, result in enumerate(gr_response.results, 1):
                print(f"{j}. {result.title} ({result.year}) - Score: {result.score:.3f}")
                print(f"   {result.explanation}")
                if result.retrieval_context and result.retrieval_context.get("graph_nodes"):
                    nodes = result.retrieval_context["graph_nodes"][:3]
                    print(f"   Graph: {nodes}")
        else:
            print("No results")

        # Query OpenMemory
        print("\n🧠 OPENMEMORY:")
        print("-" * 80)
        om_response = await openmemory.query(query, limit=3)
        print(f"Reasoning: {om_response.reasoning}\n")
        if om_response.results:
            for j, result in enumerate(om_response.results, 1):
                print(f"{j}. {result.title} ({result.year}) - Score: {result.score:.3f}")
                print(f"   {result.explanation}")
                if result.retrieval_context and result.retrieval_context.get("sectors"):
                    sectors = result.retrieval_context["sectors"]
                    print(f"   Sectors: {', '.join(sectors)}")
        else:
            print("No results")

        print()

    print("\n" + "="*80)
    print("Comparison Complete")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
