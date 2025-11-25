# Pure Vector System Design

**Date:** November 24, 2025
**Status:** Implemented (baseline system)

---

## Overview

Pure Vector is the baseline retrieval system using simple embedding similarity. No graph structure, no entity extraction - just semantic similarity in vector space.

**Purpose:** Establish baseline performance to measure improvement from more complex systems.

---

## Architecture

### Components

**1. Embedding Model**
- **Provider:** OpenAI `text-embedding-3-small`
- **Dimensions:** 1536
- **Why:** Fast, accurate, cost-effective baseline

**2. Vector Store**
- **Storage:** ChromaDB (local, in-memory)
- **Why:** Simple setup, no infrastructure dependencies
- **Index:** Cosine similarity (default)

**3. LLM Reasoning**
- **Model:** GPT-4 (configurable via settings)
- **Role:** Explain why retrieved movies match the query
- **Input:** Query + retrieved movie contexts
- **Output:** AgentResponse with explanations

---

## Storage Strategy

### Single Flat Embedding Per Movie

Each movie is converted to a single text representation and embedded:

```python
def to_text(movie: Movie) -> str:
    """Flatten all movie attributes to text."""
    parts = [
        f"{movie.title} ({movie.year})",
        f"Directed by {', '.join(movie.director)}",
        f"Genres: {', '.join(movie.genres)}",
        f"Themes: {', '.join([t.name for t in movie.themes])}",
        f"Mood: {', '.join(movie.mood.primary)}",
        f"Visual style: {', '.join(movie.visual_style.descriptors)}",
        f"Pacing: {movie.narrative.pacing}, Tone: {movie.narrative.tone}",
        movie.plot_summary,
    ]
    return " ".join(parts)
```

**Metadata stored:**
- `movie_id`: For lookup
- `title`, `year`: For display

---

## Retrieval Strategy

### Two-Stage Process

**Stage 1: Vector Search**
```python
# Embed query
query_embedding = openai.embeddings.create(
    model="text-embedding-3-small",
    input=query
).data[0].embedding

# Cosine similarity search
results = chroma_collection.query(
    query_embeddings=[query_embedding],
    n_results=limit * 2  # Get extras for LLM filtering
)
```

**Stage 2: LLM Reasoning**
- Context: Query + retrieved movie texts
- Task: Explain why each movie matches
- Output: Ranked results with explanations

---

## Strengths

✅ **Simplicity:** No complex setup, no graph extraction
✅ **Speed:** Single embedding lookup, fast retrieval
✅ **Broad recall:** Semantic similarity captures unexpected connections
✅ **Low cost:** Embeddings only (no extraction LLM calls)
✅ **Universal:** Works for any content type without schema

---

## Weaknesses

❌ **No fact-checking:** Can return semantically similar but factually wrong results
- Example: "Denis Villeneuve movies" → returns "Her" (wrong director, similar themes)
❌ **No explainability:** Can't explain relationships beyond "semantically similar"
❌ **No structured queries:** Can't leverage specific relationships (director, genre, etc.)
❌ **Single embedding:** All attributes flattened, loses fine-grained signal

---

## Comparison to Other Systems

### vs Graphiti
- **Pure Vector:** Semantic similarity only
- **Graphiti:** Explicit relationships (DIRECTED_BY, EXPLORES_THEME)
- **Tradeoff:** Pure Vector has wider recall, Graphiti has higher precision

### vs OpenMemory
- **Pure Vector:** Single embedding space
- **OpenMemory:** Multi-sector decomposition (semantic, emotional, procedural)
- **Tradeoff:** Pure Vector simpler, OpenMemory may capture different aspects better

---

## Implementation Details

### File Location
- `python/src/entertainment_graph/systems/pure_vector.py`

### Key Methods

```python
class PureVectorSystem(AgenticSystem):
    async def ingest(self, movies: list[Movie]) -> int:
        """Embed each movie's text and store in ChromaDB."""
        for movie in movies:
            text = movie.to_text()
            embedding = self._embed(text)
            self.collection.add(
                ids=[movie.id],
                embeddings=[embedding],
                metadatas=[{"title": movie.title, "year": movie.year}],
                documents=[text]
            )

    async def query(self, query: str, limit: int = 5) -> AgentResponse:
        """
        1. Embed query
        2. Vector search (cosine similarity)
        3. LLM explains results
        """
```

---

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-...  # Required for embeddings + LLM
LLM_MODEL=gpt-4        # Optional, default: gpt-4o
```

### ChromaDB Settings
- **Path:** In-memory (ephemeral) for dev, persistent for production
- **Collection:** `entertainment_movies`
- **Distance:** Cosine similarity (default)

---

## Test Queries & Expected Behavior

### Query 1: "Denis Villeneuve movies"
- **Expected:** Dune, Blade Runner 2049
- **Actual:** Also returns "Her" (wrong director, but similar themes)
- **Issue:** No fact-checking on director relationship

### Query 2: "Films similar to Blade Runner's visual style"
- **Expected:** Blade Runner 2049, Dune (same director, similar aesthetic)
- **Actual:** Good results, captures visual descriptors in embedding
- **Success:** Semantic similarity works for aesthetic queries

### Query 3: "Movies with dystopian corporate themes"
- **Expected:** Severance, Blade Runner 2049
- **Actual:** Good thematic matching via embeddings
- **Success:** Theme keywords captured in flat text

---

## Cost Analysis

**Per movie:**
- 1 embedding call (~$0.0001)

**Per query:**
- 1 embedding call (~$0.0001)
- 1 LLM call for reasoning (~$0.01)

**Total for 5 movies + 3 queries:**
- Ingestion: 5 × $0.0001 = $0.0005
- Queries: 3 × $0.0101 = $0.0303
- **Total: ~$0.03**

Cheapest system (no entity extraction overhead).

---

## Performance Characteristics

**Ingestion:**
- Fast (just embeddings, no graph extraction)
- ~1 second per movie

**Query:**
- Fast (vector lookup + 1 LLM call)
- ~2-3 seconds per query

**Scalability:**
- ChromaDB scales to millions of vectors
- Bottleneck: LLM reasoning (sequential)

---

## Future Improvements (Out of Scope for Phase 1)

1. **Multi-vector per movie:** Separate embeddings for plot, themes, mood
2. **Hybrid search:** Combine vector similarity with metadata filters
3. **Reranking:** Use cross-encoder for better ranking
4. **Query decomposition:** Break complex queries into sub-queries

---

## Related Files

- Implementation: [python/src/entertainment_graph/systems/pure_vector.py](../python/src/entertainment_graph/systems/pure_vector.py)
- Model: [python/src/entertainment_graph/models/movie.py](../python/src/entertainment_graph/models/movie.py)
- Tests: [python/test_basic.py](../python/test_basic.py)
- Comparison: [COMPARISON_RESULTS.md](../COMPARISON_RESULTS.md)

---

## Status

✅ **Implemented** - Baseline system complete
✅ **Tested** - All 3 test queries working
✅ **Compared** - Results documented in COMPARISON_RESULTS.md

**Next:** Use as baseline to evaluate Graphiti and OpenMemory improvements.
