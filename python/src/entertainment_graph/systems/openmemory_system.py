"""OpenMemory system - hierarchical memory decomposition with cognitive sectors."""

import json
from openmemory import OpenMemory
from openai import OpenAI

from entertainment_graph.config import get_settings
from entertainment_graph.models import Movie, AgentResponse, QueryResult
from .base import AgenticSystem


class OpenMemorySystem(AgenticSystem):
    """
    OpenMemory: Hierarchical memory architecture with 5 cognitive sectors.

    For entertainment discovery, we use 3 sectors:
    - Semantic: Facts, themes, genres (decay: 0.001)
    - Emotional: Mood, visual style, tone (decay: 0.01)
    - Procedural: Pacing, structure, patterns (decay: 0.002)

    Each movie is stored as 3 memories across these sectors.
    """

    def __init__(self, db_path: str = "./openmemory.sqlite", tier: str = "fast"):
        self.settings = get_settings()
        self.openai = OpenAI(api_key=self.settings.openai_api_key)
        self.openmemory = OpenMemory(
            mode="local",
            path=db_path,
            tier=tier,  # fast, smart, deep, or hybrid
            embeddings={"provider": "openai", "apiKey": self.settings.openai_api_key},
        )
        self._movies: dict[str, Movie] = {}  # Cache for movie data

    @property
    def name(self) -> str:
        return "OpenMemory"

    async def ingest(self, movies: list[Movie]) -> int:
        """Ingest movies as multi-sector memories."""
        if not movies:
            return 0

        for movie in movies:
            # Cache movie data
            self._movies[movie.id] = movie

            # Create memories for each sector
            semantic_memory = self._create_semantic_memory(movie)
            emotional_memory = self._create_emotional_memory(movie)
            procedural_memory = self._create_procedural_memory(movie)

            # Store in OpenMemory with sector-specific memories
            # OpenMemory API: add(content, tags=None, metadata=None, userId=None, salience=None, decayLambda=None)
            # Use _add_async since we're in async context (add() uses asyncio.run() internally)
            # Use tags to track sectors
            metadata = {"movie_id": movie.id, "title": movie.title, "year": str(movie.year)}

            await self.openmemory._add_async(
                content=semantic_memory,
                tags=["semantic"],
                metadata=metadata,
            )

            await self.openmemory._add_async(
                content=emotional_memory,
                tags=["emotional"],
                metadata=metadata,
            )

            await self.openmemory._add_async(
                content=procedural_memory,
                tags=["procedural"],
                metadata=metadata,
            )

        return len(movies)

    def _create_semantic_memory(self, movie: Movie) -> str:
        """
        Create semantic memory: facts, themes, genres, plot.

        Semantic sector (decay: 0.001) - stable factual knowledge.
        """
        parts = [f"{movie.title} is a {movie.year} film"]

        if movie.director:
            directors = ", ".join(movie.director)
            parts.append(f"directed by {directors}")

        if movie.genres:
            genres = ", ".join(movie.genres)
            parts.append(f"in the genres: {genres}")

        if movie.plot_summary:
            parts.append(f"Plot: {movie.plot_summary}")

        # Themes with prominence
        if movie.themes:
            theme_desc = []
            for theme in movie.themes:
                prominence = theme.prominence
                theme_desc.append(f"{prominence} theme of {theme.name}")
            parts.append(f"It explores {', '.join(theme_desc)}")

        # Narrative structure
        if movie.narrative:
            parts.append(f"The narrative has {movie.narrative.structure} structure")

        return ". ".join(parts) + "."

    def _create_emotional_memory(self, movie: Movie) -> str:
        """
        Create emotional memory: mood, visual style, tone.

        Emotional sector (decay: 0.01) - mood and aesthetic attributes.
        """
        parts = []

        # Mood
        if movie.mood:
            mood_primary = ", ".join(movie.mood.primary)
            parts.append(f"{movie.title} evokes a {mood_primary} mood")

            if movie.mood.undertones:
                undertones = ", ".join(movie.mood.undertones)
                parts.append(f"with undertones of {undertones}")

            parts.append(f"The emotional intensity is {movie.mood.intensity}")

            if movie.mood.emotional_arc:
                parts.append(f"Emotional arc: {movie.mood.emotional_arc}")

        # Visual style
        if movie.visual_style:
            if movie.visual_style.palette:
                palette = ", ".join(movie.visual_style.palette)
                parts.append(f"Visual palette includes {palette}")

            if movie.visual_style.descriptors:
                descriptors = ", ".join(movie.visual_style.descriptors)
                parts.append(f"Visual style is {descriptors}")

            if movie.visual_style.composition:
                composition = ", ".join(movie.visual_style.composition)
                parts.append(f"Composition features {composition}")

        # Tone
        if movie.narrative:
            parts.append(f"The tone is {movie.narrative.tone}")

        return ". ".join(parts) + "." if parts else f"{movie.title} has unique emotional qualities."

    def _create_procedural_memory(self, movie: Movie) -> str:
        """
        Create procedural memory: pacing, structure, similarity patterns.

        Procedural sector (decay: 0.002) - how things work, patterns.
        """
        parts = []

        # Narrative pacing and structure
        if movie.narrative:
            parts.append(
                f"{movie.title} uses {movie.narrative.pacing} pacing "
                f"with {movie.narrative.structure} structure"
            )

            if movie.narrative.perspective:
                parts.append(f"Perspective: {movie.narrative.perspective}")

        # Runtime
        if movie.runtime_minutes:
            parts.append(f"Runtime: {movie.runtime_minutes} minutes")

        # Similarity patterns
        if movie.similar_to:
            for sim in movie.similar_to:
                target_movie = self._movies.get(sim.target_id)
                target_title = target_movie.title if target_movie else sim.target_id
                parts.append(
                    f"Similar to {target_title} due to {sim.relationship_type}: {sim.explanation}"
                )

        return ". ".join(parts) + "." if parts else f"{movie.title} has unique procedural patterns."

    async def query(self, query: str, limit: int = 5) -> AgentResponse:
        """Query using multi-sector retrieval + LLM reasoning."""
        # 1. Classify query intent to determine which sectors to search
        sectors = self._classify_query_intent(query)

        # 2. Search relevant sectors
        # OpenMemory API: query(query, k=10, filters=None)
        # Use _query_async since we're in async context
        # Use filters to query by sector tags
        all_results = []
        for sector in sectors:
            sector_results = await self.openmemory._query_async(
                query=query,
                k=limit * 2,  # Get more results for filtering
                filters={"tags": [sector]},  # Filter by sector tag
            )
            if sector_results:
                all_results.extend(sector_results)

        if not all_results:
            return AgentResponse(
                results=[],
                reasoning="No relevant memories found across sectors.",
                system_name=self.name,
            )

        # 3. Extract unique movie IDs from results
        movie_contexts = self._extract_movie_contexts(all_results)

        if not movie_contexts:
            return AgentResponse(
                results=[],
                reasoning="Search returned memories but no movies could be identified.",
                system_name=self.name,
            )

        # 4. Use LLM to reason over memories and explain results
        context_text = self._format_memory_context(movie_contexts)
        llm_response = self.openai.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an entertainment recommendation assistant with access to a multi-sector memory system.

Given a user query and memory context from different cognitive sectors (semantic, emotional, procedural), explain why each movie matches.

Return a JSON object with:
- "reasoning": Brief explanation of how you interpreted the query and which sectors were most relevant
- "results": Array of objects with "id" (movie ID), "explanation" (why this movie matches, referencing specific memories)

Reference the specific sectors and memory content in your explanations.""",
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\n\nMemory context:\n{context_text}",
                },
            ],
            response_format={"type": "json_object"},
        )

        # 5. Parse LLM response
        try:
            llm_result = json.loads(llm_response.choices[0].message.content)
        except json.JSONDecodeError:
            llm_result = {"reasoning": "Failed to parse LLM response", "results": []}

        # 6. Build final response
        query_results = []
        for movie_ctx in movie_contexts[:limit]:
            movie = self._movies.get(movie_ctx["movie_id"])
            if not movie:
                continue

            # Find LLM explanation
            explanation = "Found through multi-sector memory retrieval."
            for llm_item in llm_result.get("results", []):
                if llm_item.get("id") == movie_ctx["movie_id"]:
                    explanation = llm_item.get("explanation", explanation)
                    break

            query_results.append(
                QueryResult(
                    id=movie.id,
                    title=movie.title,
                    year=movie.year,
                    score=movie_ctx.get("score", 0.8),  # OpenMemory similarity score
                    explanation=explanation,
                    retrieval_context={
                        "sectors": movie_ctx.get("sectors", []),
                        "memories": movie_ctx.get("memories", []),
                    },
                )
            )

        return AgentResponse(
            results=query_results,
            reasoning=llm_result.get("reasoning", f"Retrieved using multi-sector search across {', '.join(sectors)}."),
            system_name=self.name,
        )

    def _classify_query_intent(self, query: str) -> list[str]:
        """
        Classify query to determine which sectors to search.

        - Factual queries (directors, actors, year) → semantic
        - Mood/aesthetic queries → emotional + semantic
        - Pacing/structure queries → procedural + semantic
        - Complex queries → all sectors
        """
        query_lower = query.lower()

        # Simple heuristic-based classification
        sectors = []

        # Check for factual indicators
        factual_keywords = ["director", "directed", "actor", "year", "genre", "about", "theme"]
        if any(kw in query_lower for kw in factual_keywords):
            sectors.append("semantic")

        # Check for emotional/mood indicators
        emotional_keywords = ["mood", "feel", "aesthetic", "visual", "style", "tone", "atmosphere", "melancholic", "contemplative", "dark", "bright"]
        if any(kw in query_lower for kw in emotional_keywords):
            sectors.append("emotional")

        # Check for procedural indicators
        procedural_keywords = ["pacing", "slow", "fast", "structure", "similar to", "like"]
        if any(kw in query_lower for kw in procedural_keywords):
            sectors.append("procedural")

        # Default: search all sectors if ambiguous
        if not sectors:
            sectors = ["semantic", "emotional", "procedural"]

        # Always include semantic for context
        if "semantic" not in sectors:
            sectors.append("semantic")

        return sectors

    def _extract_movie_contexts(self, results: list) -> list[dict]:
        """
        Extract movie contexts from OpenMemory results.

        OpenMemory returns memories with metadata including movie_id.
        """
        movie_contexts = {}

        for result in results:
            # OpenMemory results have 'meta' field as JSON string
            meta_str = result.get("meta", "{}")
            try:
                metadata = json.loads(meta_str)
            except json.JSONDecodeError:
                continue

            movie_id = metadata.get("movie_id")

            if not movie_id or movie_id not in self._movies:
                continue

            if movie_id not in movie_contexts:
                movie_contexts[movie_id] = {
                    "movie_id": movie_id,
                    "sectors": [],
                    "memories": [],
                    "score": 0.0,
                }

            # Track which sector this memory came from (from tags)
            tags_str = result.get("tags", "[]")
            try:
                tags = json.loads(tags_str)
                for tag in tags:
                    if tag not in movie_contexts[movie_id]["sectors"]:
                        movie_contexts[movie_id]["sectors"].append(tag)
            except json.JSONDecodeError:
                pass

            # Add memory content
            content = result.get("content", "")
            if content and content not in movie_contexts[movie_id]["memories"]:
                movie_contexts[movie_id]["memories"].append(content)

            # Update score (use max similarity across sectors)
            similarity = result.get("score", 0.0)
            movie_contexts[movie_id]["score"] = max(
                movie_contexts[movie_id]["score"], similarity
            )

        # Sort by score descending
        sorted_contexts = sorted(
            movie_contexts.values(), key=lambda x: x["score"], reverse=True
        )

        return sorted_contexts

    def _format_memory_context(self, movie_contexts: list[dict]) -> str:
        """Format movie contexts for LLM."""
        formatted = []
        for ctx in movie_contexts:
            movie = self._movies.get(ctx["movie_id"])
            if movie:
                formatted.append(f"\nMovie: {movie.title} ({movie.year})")
                formatted.append(f"  ID: {ctx['movie_id']}")
                formatted.append(f"  Sectors: {', '.join(ctx['sectors'])}")
                formatted.append(f"  Score: {ctx['score']:.3f}")
                for i, memory in enumerate(ctx["memories"][:3], 1):  # Show top 3 memories
                    formatted.append(f"  Memory {i}: {memory}")
        return "\n".join(formatted)

    async def health_check(self) -> bool:
        """Check if OpenMemory is available."""
        try:
            # Simple test query
            self.openmemory.query(query="test", k=1)
            return True
        except Exception:
            return False

    async def clear(self) -> None:
        """Clear all memories and movie cache."""
        # OpenMemory stores data in local SQLite - need to reinitialize
        # Get the current path from openmemory instance
        db_path = getattr(self.openmemory, 'path', './openmemory.sqlite')
        self.openmemory = OpenMemory(
            mode="local",
            path=db_path,
            tier="fast",
            embeddings={"provider": "openai", "apiKey": self.settings.openai_api_key},
        )
        self._movies.clear()
