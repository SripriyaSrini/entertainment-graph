# Graphiti System Design

**Date:** November 24, 2025
**Status:** Implemented

---

## Overview

Graphiti is a temporal knowledge graph system with automatic entity and relationship extraction. It uses LLMs to extract structured knowledge from unstructured text and stores it in Neo4j.

**Key Feature:** Explicit relationships (not just semantic similarity) + temporal awareness.

---

## Architecture

### Components

**1. Entity Extraction**
- **Method:** LLM-based (automatic via Graphiti)
- **Entities:** Movies, directors, themes, moods, visual styles
- **Extraction:** From rich episode text describing each movie

**2. Relationship Extraction**
- **Method:** LLM infers relationships from text
- **Types:** `DIRECTED_BY`, `EXPLORES_THEME`, `HAS_MOOD`, `SIMILAR_TO_VISUAL_STYLE`, etc.
- **Storage:** Neo4j edges with properties

**3. Graph Database**
- **Storage:** Neo4j Aura (managed cloud)
- **Why:** Native graph operations, Cypher queries, temporal indexing
- **Indices:** Built via `graphiti.build_indices_and_constraints()`

**4. Hybrid Retrieval**
- **Semantic:** Vector embeddings of entities/facts
- **BM25:** Keyword matching
- **Graph Traversal:** Follow edges from matched nodes

**5. LLM Reasoning**
- **Model:** GPT-4
- **Input:** Query + graph context (nodes, edges, facts)
- **Output:** Explained results with graph evidence

---

## Storage Strategy

### Episode-Based Ingestion

Each movie is stored as an **episode** - a timestamped narrative that Graphiti extracts entities/relationships from:

```python
def _create_episode_text(movie: Movie) -> str:
    """Rich text for Graphiti to extract from."""
    parts = [
        f"{movie.title} is a {movie.year} film",
        f"directed by {', '.join(movie.director)}",
        f"in the genres: {', '.join(movie.genres)}",
        f"It explores {prominence} theme of {theme.name}",  # For each theme
        f"The mood is {', '.join(movie.mood.primary)}",
        f"Visual style is {', '.join(movie.visual_style.descriptors)}",
        f"The narrative has {movie.narrative.pacing} pacing",
        f"It is similar to {target} due to {relationship_type}: {explanation}",
    ]
    return ". ".join(parts) + "."
```

**Graphiti's LLM automatically extracts:**
- **Entities:** "Blade Runner 2049", "Denis Villeneuve", "identity", "neo-noir"
- **Relationships:**
  - `(Blade Runner 2049)-[:DIRECTED_BY]->(Denis Villeneuve)`
  - `(Blade Runner 2049)-[:EXPLORES_THEME]->(identity)`
  - `(Blade Runner 2049)-[:HAS_VISUAL_STYLE]->(neo-noir)`

---

## Retrieval Strategy

### Three-Stage Hybrid Process

**Stage 1: Hybrid Search**
```python
search_results = await graphiti.search(
    query="Denis Villeneuve movies",
    num_results=limit * 2
)
# Returns: nodes, edges, episodes that match
```

Graphiti combines:
1. **Vector similarity:** Query embedding vs entity embeddings
2. **BM25:** Keyword matching on fact text
3. **Graph traversal:** Nodes connected to matched entities

**Stage 2: Extract Movie Context**
- Map graph nodes/edges back to movies
- Gather relationship evidence

**Stage 3: LLM Reasoning**
- Context: Query + graph nodes + relationships
- Task: Explain matches using graph structure
- Output: Results with explicit relationship evidence

---

## Strengths

✅ **Factual accuracy:** Explicit relationships prevent false positives
- Example: "Denis Villeneuve movies" uses `DIRECTED_BY` edge (100% accurate)
✅ **Explainability:** Can show exact graph path (not just "similar")
- Example: "Found via DIRECTED_BY relationship to Denis Villeneuve"
✅ **Structured queries:** Can leverage specific relationship types
✅ **Temporal awareness:** Tracks when facts were added (not used in Phase 1)
✅ **Graph reasoning:** Can do multi-hop queries (movies by same director who worked with actor X)

---

## Weaknesses

❌ **Extraction overhead:** LLM calls for every movie during ingestion
- Cost: ~4x more expensive than Pure Vector
- Speed: Slower ingestion (~5-10 seconds per movie)
❌ **Lower recall:** Only returns movies with explicit relationships
- Example: "Films similar to Blade Runner's visual style" → only 1 result (Blade Runner 2049)
- Pure Vector found 3 results (included Dune via semantic similarity)
❌ **Extraction quality:** Depends on episode text quality and LLM accuracy
❌ **Infrastructure:** Requires Neo4j (cloud or local), not just local storage

---

## Comparison to Other Systems

### vs Pure Vector
- **Graphiti:** Explicit `DIRECTED_BY` → 100% precision on factual queries
- **Pure Vector:** Semantic similarity → false positives (returned "Her" for Villeneuve query)
- **Tradeoff:** Graphiti trades recall for precision

### vs OpenMemory
- **Graphiti:** Graph relationships (explicit edges)
- **OpenMemory:** Multi-sector decomposition (implicit cognitive structure)
- **Tradeoff:** Graphiti better for factual queries, OpenMemory may capture nuanced attributes better

---

## Implementation Details

### File Location
- `python/src/entertainment_graph/systems/graphiti_system.py`

### Key Methods

```python
class GraphitiSystem(AgenticSystem):
    async def ingest(self, movies: list[Movie]) -> int:
        """Create episode per movie, Graphiti extracts entities/relationships."""
        for movie in movies:
            episode_text = self._create_episode_text(movie)
            await self.graphiti.add_episode(
                name=f"Movie: {movie.title}",
                episode_body=episode_text,
                reference_time=datetime(movie.year, 1, 1),
                source=EpisodeType.text,
            )

    async def query(self, query: str, limit: int = 5) -> AgentResponse:
        """
        1. Hybrid search (vector + BM25 + graph)
        2. Extract movie contexts from graph results
        3. LLM explains using graph relationships
        """
        search_results = await self.graphiti.search(query, num_results=limit * 2)
        movie_contexts = self._extract_movie_contexts(search_results)
        # LLM reasoning with graph context...
```

---

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=sk-...           # Required for Graphiti's LLM extraction
NEO4J_URI=neo4j+s://...         # Neo4j Aura connection
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=...
LLM_MODEL=gpt-4                 # Optional
```

### Neo4j Setup
- **Provider:** Neo4j Aura (free tier: 200MB, sufficient for Phase 1)
- **Indices:** Created via `graphiti.build_indices_and_constraints()`
- **Schema:** Dynamic (Graphiti creates nodes/edges as needed)

---

## Test Queries & Expected Behavior

### Query 1: "Denis Villeneuve movies"
- **Expected:** Dune, Blade Runner 2049
- **Actual:** Exactly those 2 (via `DIRECTED_BY` relationship)
- **Success:** 100% precision, no false positives

### Query 2: "Films similar to Blade Runner's visual style"
- **Expected:** Blade Runner 2049, possibly Dune
- **Actual:** Only Blade Runner 2049 (explicit `SIMILAR_TO_VISUAL_STYLE` edge)
- **Issue:** Lower recall - Dune not returned (no explicit visual similarity extracted)

### Query 3: "Movies with dystopian corporate themes"
- **Expected:** Severance, Blade Runner 2049
- **Actual:** Good results via `EXPLORES_THEME` edges
- **Success:** Thematic relationships captured

---

## Extracted Relationships (Examples)

From the 5 sample movies, Graphiti extracted:

```cypher
// Director relationships
(Blade Runner 2049)-[:DIRECTED_BY]->(Denis Villeneuve)
(Dune)-[:DIRECTED_BY]->(Denis Villeneuve)
(Her)-[:DIRECTED_BY]->(Spike Jonze)

// Theme relationships
(Severance)-[:EXPLORES_THEME]->(corporate control)
(Blade Runner 2049)-[:EXPLORES_THEME]->(identity)
(Her)-[:EXPLORES_THEME]->(loneliness)

// Visual style relationships
(Blade Runner 2049)-[:SIMILAR_TO_VISUAL_STYLE]->(Blade Runner)

// Thematic links
(Blade Runner 2049)-[:THEMATIC_LINKS]->(dystopian futures)
(Severance)-[:THEMATIC_LINKS]->(corporate control)
```

---

## Cost Analysis

**Per movie:**
- Episode ingestion: 1-3 LLM calls for extraction (~$0.01-0.03)
- Entity/relationship extraction: Automatic via Graphiti

**Per query:**
- 1 hybrid search (included)
- 1 LLM call for reasoning (~$0.01)

**Total for 5 movies + 3 queries:**
- Ingestion: 5 × $0.02 = $0.10
- Queries: 3 × $0.01 = $0.03
- **Total: ~$0.13**

~4x more expensive than Pure Vector due to extraction.

---

## Performance Characteristics

**Ingestion:**
- Slow (LLM extraction per movie)
- ~5-10 seconds per movie
- Parallel processing possible but limited by LLM rate limits

**Query:**
- Moderate speed (hybrid search + graph traversal + 1 LLM call)
- ~3-5 seconds per query

**Scalability:**
- Neo4j scales to billions of nodes/edges
- Bottleneck: Ingestion LLM calls (can parallelize)

---

## Temporal Features (Not Used in Phase 1)

Graphiti tracks `valid_at` timestamps for all facts:
- When was "Denis Villeneuve directed Dune" added?
- Query: "What directors were active in 2021?"

**Phase 2 use case:** Track when user watched movies, preference changes over time.

---

## Future Improvements (Out of Scope for Phase 1)

1. **Multi-hop queries:** "Movies by directors who worked on sci-fi in the 2010s"
2. **Temporal queries:** "Recently added films in X genre"
3. **Relationship inference:** Infer transitive relationships (if A similar to B, B similar to C...)
4. **Custom extraction prompts:** Guide Graphiti to extract specific relationship types

---

## Related Files

- Implementation: [python/src/entertainment_graph/systems/graphiti_system.py](../python/src/entertainment_graph/systems/graphiti_system.py)
- Model: [python/src/entertainment_graph/models/movie.py](../python/src/entertainment_graph/models/movie.py)
- Tests: [python/test_graphiti.py](../python/test_graphiti.py)
- Comparison: [COMPARISON_RESULTS.md](../COMPARISON_RESULTS.md)

---

## Status

✅ **Implemented** - Full Graphiti integration complete
✅ **Tested** - All 3 test queries working
✅ **Compared** - 100% factual accuracy vs 67% for Pure Vector on director query

**Key Finding:** Graphiti trades recall for precision - excellent for factual queries, but may miss semantically similar results without explicit relationships.

---

## References

- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [Graphiti Docs](https://help.getzep.com/graphiti)
- [Neo4j Aura](https://neo4j.com/cloud/aura/)
