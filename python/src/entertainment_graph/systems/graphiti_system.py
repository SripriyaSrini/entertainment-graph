"""Graphiti system - temporal knowledge graph with entity/relationship extraction."""

import json
from datetime import datetime
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from openai import OpenAI

from entertainment_graph.config import get_settings
from entertainment_graph.models import Movie, AgentResponse, QueryResult
from .base import AgenticSystem


class GraphitiSystem(AgenticSystem):
    """
    Graphiti: Temporal knowledge graph with automatic entity/relationship extraction.

    - Automatically extracts entities (movies, directors, themes) from text
    - Creates relationships between entities
    - Provides hybrid search (semantic + BM25 + graph traversal)
    - Temporal awareness (tracks when facts were added)
    """

    def __init__(self):
        self.settings = get_settings()
        self.openai = OpenAI(api_key=self.settings.openai_api_key)

        # Initialize Graphiti with Neo4j
        self.graphiti = Graphiti(
            uri=self.settings.neo4j_uri,
            user=self.settings.neo4j_username,
            password=self.settings.neo4j_password,
        )

        self._movies: dict[str, Movie] = {}  # Cache for movie data
        self._initialized = False

    @property
    def name(self) -> str:
        return "Graphiti"

    async def _ensure_initialized(self):
        """Ensure Graphiti indices are built (one-time setup)."""
        if not self._initialized:
            await self.graphiti.build_indices_and_constraints()
            self._initialized = True

    async def ingest(self, movies: list[Movie]) -> int:
        """Ingest movies as episodes into Graphiti."""
        await self._ensure_initialized()

        if not movies:
            return 0

        for movie in movies:
            # Cache movie data
            self._movies[movie.id] = movie

            # Create episode text - Graphiti will extract entities/relationships
            episode_text = self._create_episode_text(movie)

            # Add episode to Graphiti
            await self.graphiti.add_episode(
                name=f"Movie: {movie.title}",
                episode_body=episode_text,
                reference_time=datetime(movie.year, 1, 1),  # Use movie year as timestamp
                source_description=f"Movie data for {movie.title} (ID: {movie.id})",
                source=EpisodeType.text,
            )

        return len(movies)

    def _create_episode_text(self, movie: Movie) -> str:
        """
        Create rich text description for Graphiti to extract entities/relationships.

        Graphiti's LLM will automatically extract:
        - Entities: movie title, directors, themes, mood descriptors
        - Relationships: directed_by, has_theme, similar_to, etc.
        """
        parts = [
            f"{movie.title} is a {movie.year} film",
        ]

        if movie.director:
            directors = ", ".join(movie.director)
            parts.append(f"directed by {directors}")

        if movie.genres:
            genres = ", ".join(movie.genres)
            parts.append(f"in the genres: {genres}")

        # Themes with prominence
        if movie.themes:
            theme_desc = []
            for theme in movie.themes:
                prominence = theme.prominence
                theme_desc.append(f"{prominence} theme of {theme.name}")
            parts.append(f"It explores {', '.join(theme_desc)}")

        # Mood
        if movie.mood:
            mood_primary = ", ".join(movie.mood.primary)
            parts.append(f"The mood is {mood_primary}")
            if movie.mood.undertones:
                undertones = ", ".join(movie.mood.undertones)
                parts.append(f"with undertones of {undertones}")
            parts.append(f"The intensity is {movie.mood.intensity}")

        # Visual style
        if movie.visual_style:
            if movie.visual_style.palette:
                palette = ", ".join(movie.visual_style.palette)
                parts.append(f"Visual palette includes {palette}")
            if movie.visual_style.descriptors:
                descriptors = ", ".join(movie.visual_style.descriptors)
                parts.append(f"Visual style is {descriptors}")

        # Narrative
        if movie.narrative:
            parts.append(
                f"The narrative has {movie.narrative.pacing} pacing, "
                f"{movie.narrative.structure} structure, and {movie.narrative.tone} tone"
            )

        # Similarity relationships
        if movie.similar_to:
            for sim in movie.similar_to:
                target_movie = self._movies.get(sim.target_id)
                target_title = target_movie.title if target_movie else sim.target_id
                parts.append(
                    f"It is similar to {target_title} due to {sim.relationship_type}: {sim.explanation}"
                )

        return ". ".join(parts) + "."

    async def query(self, query: str, limit: int = 5) -> AgentResponse:
        """Query using Graphiti's hybrid search + LLM reasoning."""
        await self._ensure_initialized()

        # 1. Search Graphiti's knowledge graph
        # This uses hybrid retrieval: semantic embeddings + BM25 + graph traversal
        search_results = await self.graphiti.search(
            query=query,
            num_results=limit * 2,  # Get more results for filtering
        )

        if not search_results:
            return AgentResponse(
                results=[],
                reasoning="No relevant information found in the knowledge graph.",
                system_name=self.name,
            )

        # 2. Extract movie IDs from search results
        # Graphiti returns nodes, edges, and episodes - we need to map back to movies
        movie_contexts = self._extract_movie_contexts(search_results)

        if not movie_contexts:
            return AgentResponse(
                results=[],
                reasoning="Search returned graph nodes but no movies could be identified.",
                system_name=self.name,
            )

        # 3. Use LLM to reason over graph context and explain results
        context_text = self._format_graph_context(movie_contexts)
        llm_response = self.openai.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an entertainment recommendation assistant with access to a knowledge graph.

Given a user query and graph context (entities, relationships, temporal info), explain why each movie matches.

Return a JSON object with:
- "reasoning": Brief explanation of how you interpreted the query and used the graph
- "results": Array of objects with "id" (movie ID), "explanation" (why this movie matches, referencing graph relationships)

Be specific about graph relationships, shared entities, and temporal patterns.""",
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\n\nGraph context:\n{context_text}",
                },
            ],
            response_format={"type": "json_object"},
        )

        # 4. Parse LLM response
        try:
            llm_result = json.loads(llm_response.choices[0].message.content)
        except json.JSONDecodeError:
            llm_result = {"reasoning": "Failed to parse LLM response", "results": []}

        # 5. Build final response
        query_results = []
        for movie_ctx in movie_contexts[:limit]:
            movie = self._movies.get(movie_ctx["movie_id"])
            if not movie:
                continue

            # Find LLM explanation
            explanation = "Found through graph traversal and entity relationships."
            for llm_item in llm_result.get("results", []):
                if llm_item.get("id") == movie_ctx["movie_id"]:
                    explanation = llm_item.get("explanation", explanation)
                    break

            query_results.append(
                QueryResult(
                    id=movie.id,
                    title=movie.title,
                    year=movie.year,
                    score=movie_ctx.get("score", 0.8),  # Graphiti doesn't provide scores directly
                    explanation=explanation,
                    retrieval_context={
                        "graph_nodes": movie_ctx.get("entities", []),
                        "relationships": movie_ctx.get("relationships", []),
                    },
                )
            )

        return AgentResponse(
            results=query_results,
            reasoning=llm_result.get("reasoning", "Retrieved using graph traversal and hybrid search."),
            system_name=self.name,
        )

    def _extract_movie_contexts(self, search_results) -> list[dict]:
        """
        Extract movie contexts from Graphiti search results.

        Graphiti returns a mix of nodes (entities) and edges (relationships).
        We need to identify which movies are referenced and gather their context.
        """
        movie_contexts = {}

        for result in search_results:
            # Graphiti search results contain nodes and edges
            # Each result has attributes like: name, fact, uuid, valid_at, etc.

            # Try to extract movie ID by matching movie title in the result
            movie_id = None
            for mid, movie in self._movies.items():
                result_text = ""
                if hasattr(result, "name"):
                    result_text += str(result.name)
                if hasattr(result, "fact"):
                    result_text += str(result.fact)

                if movie.title.lower() in result_text.lower():
                    movie_id = mid
                    break

            if movie_id and movie_id in self._movies:
                if movie_id not in movie_contexts:
                    movie_contexts[movie_id] = {
                        "movie_id": movie_id,
                        "entities": [],
                        "relationships": [],
                        "score": 0.85,  # Default score
                    }

                # Add entity/relationship info
                if hasattr(result, "name"):
                    movie_contexts[movie_id]["entities"].append(str(result.name))
                if hasattr(result, "fact"):
                    movie_contexts[movie_id]["relationships"].append(str(result.fact))

        return list(movie_contexts.values())

    def _format_graph_context(self, movie_contexts: list[dict]) -> str:
        """Format movie contexts for LLM."""
        formatted = []
        for ctx in movie_contexts:
            movie = self._movies.get(ctx["movie_id"])
            if movie:
                formatted.append(f"\nMovie: {movie.title} ({movie.year})")
                formatted.append(f"  ID: {ctx['movie_id']}")
                if ctx.get("entities"):
                    formatted.append(f"  Entities: {', '.join(ctx['entities'][:5])}")
                if ctx.get("relationships"):
                    formatted.append(f"  Relationships: {', '.join(ctx['relationships'][:3])}")
        return "\n".join(formatted)

    async def health_check(self) -> bool:
        """Check if Graphiti/Neo4j is available."""
        try:
            # Simple query to check connection
            await self.graphiti.search(query="test", num_results=1)
            return True
        except Exception:
            return False

    async def clear(self) -> None:
        """Clear all data from Graphiti."""
        # Graphiti doesn't have a built-in clear method
        # We'd need to delete all nodes/edges from Neo4j directly
        # For now, we'll clear the cache
        self._movies.clear()
        # TODO: Implement Neo4j clear via driver
