"""Pure Vector system - baseline using ChromaDB + OpenAI embeddings + LLM."""

import json
import chromadb
from openai import OpenAI

from entertainment_graph.config import get_settings
from entertainment_graph.models import Movie, AgentResponse, QueryResult
from .base import AgenticSystem


class PureVectorSystem(AgenticSystem):
    """
    Baseline system: embed content as vectors, retrieve by similarity, LLM explains.

    No memory structure, no graph, no temporal awareness.
    This represents what most simple RAG systems do.
    """

    def __init__(self):
        self.settings = get_settings()
        self.openai = OpenAI(api_key=self.settings.openai_api_key)
        self.chroma = chromadb.PersistentClient(path=self.settings.chroma_dir)
        self.collection = self.chroma.get_or_create_collection(
            name="movies",
            metadata={"hnsw:space": "cosine"},
        )
        self._movies: dict[str, Movie] = {}  # Cache for movie data

    @property
    def name(self) -> str:
        return "Pure Vector"

    def _get_embedding(self, text: str) -> list[float]:
        """Get embedding from OpenAI."""
        response = self.openai.embeddings.create(
            model=self.settings.embedding_model,
            input=text,
        )
        return response.data[0].embedding

    async def ingest(self, movies: list[Movie]) -> int:
        """Ingest movies into ChromaDB."""
        if not movies:
            return 0

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for movie in movies:
            text = movie.to_text()
            ids.append(movie.id)
            documents.append(text)
            embeddings.append(self._get_embedding(text))
            metadatas.append({
                "title": movie.title,
                "year": movie.year,
                "genres": json.dumps(movie.genres),
                "director": json.dumps(movie.director),
            })
            self._movies[movie.id] = movie

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(movies)

    async def query(self, query: str, limit: int = 5) -> AgentResponse:
        """Query with vector similarity, then LLM explains results."""
        # 1. Embed query and find similar movies
        query_embedding = self._get_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            include=["documents", "metadatas", "distances"],
        )

        if not results["ids"] or not results["ids"][0]:
            return AgentResponse(
                results=[],
                reasoning="No movies found in the database.",
                system_name=self.name,
            )

        # 2. Build context for LLM
        retrieved_movies = []
        for i, movie_id in enumerate(results["ids"][0]):
            movie = self._movies.get(movie_id)
            if movie:
                distance = results["distances"][0][i] if results["distances"] else 0
                similarity = 1 - distance  # cosine distance to similarity
                retrieved_movies.append({
                    "id": movie_id,
                    "title": movie.title,
                    "year": movie.year,
                    "text": results["documents"][0][i],
                    "similarity": round(similarity, 3),
                })

        # 3. LLM generates explanations
        context = json.dumps(retrieved_movies, indent=2)
        llm_response = self.openai.chat.completions.create(
            model=self.settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an entertainment recommendation assistant.
Given a user query and retrieved movies with their descriptions, explain why each movie matches the query.

Return a JSON object with:
- "reasoning": Brief explanation of how you interpreted the query
- "results": Array of objects with "id", "explanation" (why this movie matches)

Be specific about what aspects of each movie connect to the query. Focus on themes, mood, style, or other semantic connections.""",
                },
                {
                    "role": "user",
                    "content": f"Query: {query}\n\nRetrieved movies:\n{context}",
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
        for movie_data in retrieved_movies:
            # Find LLM explanation for this movie
            explanation = "Similar content based on vector similarity."
            for llm_item in llm_result.get("results", []):
                if llm_item.get("id") == movie_data["id"]:
                    explanation = llm_item.get("explanation", explanation)
                    break

            movie = self._movies.get(movie_data["id"])
            if movie:
                query_results.append(
                    QueryResult(
                        id=movie_data["id"],
                        title=movie.title,
                        year=movie.year,
                        score=movie_data["similarity"],
                        explanation=explanation,
                        retrieval_context={"similarity": movie_data["similarity"]},
                    )
                )

        return AgentResponse(
            results=query_results,
            reasoning=llm_result.get("reasoning", "Retrieved by vector similarity."),
            system_name=self.name,
        )

    async def health_check(self) -> bool:
        """Check if ChromaDB and OpenAI are available."""
        try:
            # Check ChromaDB
            self.collection.count()
            # Check OpenAI
            self._get_embedding("test")
            return True
        except Exception:
            return False

    async def clear(self) -> None:
        """Clear all data."""
        self.chroma.delete_collection("movies")
        self.collection = self.chroma.get_or_create_collection(
            name="movies",
            metadata={"hnsw:space": "cosine"},
        )
        self._movies.clear()
