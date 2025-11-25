# Entertainment Graph - Progress Summary

**Date:** November 25, 2025
**Phase:** Phase 1 - System Comparison
**Status:** 3 of 3 systems implemented and tested ✅

---

## What We're Building

A Graph RAG system for entertainment discovery that helps users find movies/shows through semantic relationships. Before building our own solution, we're comparing existing systems to understand tradeoffs.

**Approach:** Spec-driven development, no vibe coding. All decisions documented before implementation.

---

## Phase 1 Goal

Compare 3 retrieval systems empirically:
1. **Pure Vector (ChromaDB)** - Baseline: simple semantic similarity
2. **Graphiti (Neo4j)** - Temporal knowledge graph with entity extraction
3. **OpenMemory** - Multi-sector memory decomposition (semantic, emotional, procedural)

Each system ingests 50 movies with rich semantic data (themes, mood, visual style) and we query them with identical test cases to measure results.

---

## Current Status

### ✅ Completed

**Infrastructure:**
- FastAPI backend with unified `AgenticSystem` interface
- Movie data models with semantic fields (themes, mood, visual_style, narrative)
- 5 sample movies with full metadata
- Environment setup: OpenAI API, Neo4j Aura, ChromaDB

**Systems Implemented:**

1. **Pure Vector System** ✅
   - Embeddings: OpenAI text-embedding-3-small
   - Storage: ChromaDB (local)
   - Retrieval: Cosine similarity + LLM reasoning
   - Status: Working

2. **Graphiti System** ✅
   - Entity extraction: Automatic via Graphiti's LLM
   - Storage: Neo4j Aura (cloud)
   - Retrieval: Hybrid (semantic + BM25 + graph traversal)
   - Relationships extracted: `DIRECTED_BY`, `EXPLORES_THEME`, `SIMILAR_TO_VISUAL_STYLE`, etc.
   - Status: Working

3. **OpenMemory System** ✅
   - Multi-sector decomposition: Semantic, Emotional, Procedural
   - Storage: OpenMemory (local SQLite + embeddings)
   - Retrieval: Sector-based query classification + LLM reasoning
   - Sector tagging: Each movie stored as 3 separate memories (one per sector)
   - Status: Working

**Testing:**
- Individual system tests: All 3 passing
- Three-way comparison: Complete ✅
- Test queries: 3 sample queries evaluated across all systems

---

## Key Findings

### Three-Way System Comparison

**Query 1: "Movies with dystopian corporate themes"**
- **Pure Vector**: 3 results (Severance, Blade Runner 2049, Dune) - Broad semantic matching
- **Graphiti**: 2 results - Used `EXPLORES_THEME` relationship for corporate control
- **OpenMemory**: 2 results - Retrieved from emotional + procedural sectors, explained dehumanizing workplace dynamics

**Query 2: "Films similar to Blade Runner's visual style"**
- **Pure Vector**: 3 results (wide recall including thematically similar films)
- **Graphiti**: 1 result - Precise `SIMILAR_TO_VISUAL_STYLE` relationship
- **OpenMemory**: 2 results - Used **emotional sector** for visual palette (desaturated tones, neon accents), referenced monumental composition

**Query 3: "Denis Villeneuve movies"**
- **Pure Vector**: Returned "Her" (WRONG - directed by Spike Jonze) ❌
- **Graphiti**: 2 correct results via `DIRECTED_BY` relationship ✅
- **OpenMemory**: 2 correct results using **semantic sector** for director facts ✅

### System Strengths Summary

| System | Best For | Key Advantage | Weakness |
|--------|----------|---------------|----------|
| **Pure Vector** | Exploratory queries, "vibes" | Wide recall, simple, fast | False positives on factual queries |
| **Graphiti** | Factual queries, precision | Explicit relationships, 100% accuracy | Lower recall, slower ingestion |
| **OpenMemory** | Multi-faceted queries | Sector-based retrieval (semantic/emotional/procedural) | Requires sector classification strategy |

### Key Insights

1. **Factual accuracy**: Graphiti and OpenMemory both nailed director queries (100%), Pure Vector failed
2. **Visual style queries**: OpenMemory's emotional sector specifically captured visual palette details
3. **Explainability**: All 3 provide LLM-powered explanations, but Graphiti and OpenMemory reference structured context (graph edges, sectors)
4. **Recall vs Precision**: Pure Vector has highest recall (3 results), Graphiti highest precision (1-2 highly relevant)

**Verdict:** No single winner - each excels at different query types. Hybrid approach combining all three likely optimal.

---

## What's Next

### Pending Work

1. ✅ ~~**OpenMemory System**~~ - Complete
2. **Expand dataset** - 5 → 50 movies with semantic data
3. **Full evaluation** - Run 20 test queries across all systems
4. **Comparison UI** - React frontend for side-by-side evaluation
5. **Create detailed comparison results document** - Consolidate findings from all 3 systems

### Decision Point

After Phase 1 evaluation, decide on Phase 2 architecture based on empirical evidence.

---

## Project Structure

```
entertainment-graph/
├── specs/
│   └── phase1.md              # Complete Phase 1 specification
├── python/
│   ├── src/entertainment_graph/
│   │   ├── models/
│   │   │   ├── movie.py       # Movie schema with semantic data
│   │   │   └── query.py       # AgentResponse model
│   │   ├── systems/
│   │   │   ├── base.py        # AgenticSystem interface
│   │   │   ├── pure_vector.py # ChromaDB + embeddings
│   │   │   ├── graphiti_system.py # Neo4j graph + LLM extraction
│   │   │   └── openmemory_system.py # Multi-sector memory
│   │   ├── routers/           # FastAPI endpoints
│   │   └── main.py            # FastAPI app
│   ├── data/movies/           # 5 sample movie JSON files
│   ├── compare_systems.py     # Three-way comparison script
│   └── pyproject.toml         # Dependencies
└── README.md
```

---

## Running the Code

### Prerequisites
```bash
# Python 3.11
brew install python@3.11

# Dependencies
cd python
pip install -e .

# Environment variables (.env)
OPENAI_API_KEY=your_key
NEO4J_URI=neo4j+s://...
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

### Test Individual Systems
```bash
# Pure Vector
python test_basic.py

# Graphiti
python test_graphiti.py
```

### Compare Systems
```bash
python compare_systems.py
```

Output shows side-by-side results for 3 queries.

---

## Key Technical Decisions

### Decision 1: Mem0 Removed from Phase 1
- **Why**: Mem0's LLM extraction optimized for user conversations, not static content
- **Tested**: Multiple approaches all returned empty results for movie descriptions
- **Impact**: Phase 1 compares 3 systems instead of 4
- **Future**: Mem0 may be useful for Phase 2 user interaction tracking

### Decision 2: Constrained Relationships (Phase 1)
- **Current**: 8 relationship types (enum: `thematic`, `visual_style`, `creator`, etc.)
- **Why**: Consistent ground truth for comparison
- **Phase 2**: Free-form natural language edges

### Decision 3: Agentic Retrieval
- All systems include LLM reasoning, not just raw retrieval
- Flow: Query → System retrieves context → LLM reasons → Explained results

---

## Resources

**Documentation:**
- Full spec: `specs/phase1.md`
- System comparison results: Run `python compare_systems.py`

**External:**
- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [OpenMemory GitHub](https://github.com/CaviraOSS/OpenMemory)
- [ChromaDB Docs](https://docs.trychroma.com)

---

## Contact

For questions about implementation or to continue Phase 1 work, see:
- Codebase: `/Users/sripriyasrinivasan/projects/entertainment-graph`
- Spec: `specs/phase1.md`
- This summary: `PROGRESS.md`
