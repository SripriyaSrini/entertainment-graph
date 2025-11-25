# Phase 1: Comparison Framework

## Goal

Before building our own Entertainment Graph, learn from existing tools by running the same dataset through multiple systems, querying each with identical test cases, and measuring results.

**Outcome**: Informed decisions about our own architecture based on empirical evidence.

---

## Decisions

### Why Compare First

We chose **compare first, then build** over vibe coding because:
- Understanding tradeoffs before committing
- Clear baseline to measure improvement
- Learn patterns from existing implementations
- Decisions documented, not guessed

### What We're Comparing (3 Systems)

| System | Type | Why |
|--------|------|-----|
| **Pure Vector (Chroma)** | Embedding similarity | Baseline - what simple RAG achieves |
| **Graphiti (Zep)** | Temporal knowledge graph | Graph-first, explicit entity/relationship extraction |
| **OpenMemory (CaviraOSS)** | Hierarchical Memory Decomposition | Multi-sector memory architecture |

**Why only 3 systems?** Originally planned 4 including Mem0, but discovered Mem0's LLM extraction is optimized for user conversations, not static content ingestion. With `infer=False`, Mem0 becomes identical to Pure Vector. See "Decision: Mem0 Removed" section below for full investigation. Mem0 will be valuable for Phase 2+ user interaction tracking.

### Infrastructure

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Graph DB | Neo4j Aura (free tier) | Managed, no Docker, works with Mem0 + Graphiti |
| Vector Store | Chroma (local) | Simple, in-memory for dev |
| Embeddings | OpenAI text-embedding-3-small | Consistent across all systems |
| LLM | GPT-4 (same for all) | Fair comparison of system capabilities |

### Phase Scope

| Decision | Phase 1 | Phase 2 |
|----------|---------|---------|
| Relationships | Constrained enum (8 types) | Free-form natural language edges |
| Content | Movies only (50 titles) | Movies + TV + extensible |
| Users | Single user (content KB) | Multi-user with personalization |
| Language | Python only | Python + Rust (perf-critical) |

---

## Agentic Retrieval

We compare systems in **agentic mode** - with an LLM in the loop, not just raw retrieval.

```
User Query → LLM Agent + System Memory → Reasons + Retrieves → Response with Explanation
```

Each system provides different context to the LLM:

| System | What It Provides to LLM |
|--------|------------------------|
| Pure Vector + LLM | Similar documents (no structure) |
| Graphiti Agent | Nodes, edges, temporal context |
| OpenMemory Agent | Cognitive sectors + waypoint traces |

---

## Dataset

### Scope

- **50 movies** you know well (enables accurate judgment)
- Rich semantic data: themes, mood, visual style, narrative
- Ground truth `similar_to` links for evaluation

### Movie Schema

```typescript
interface Movie {
  id: string;                    // "blade-runner-2049"
  title: string;
  year: number;
  genres: string[];
  director: string[];

  // Semantic data (LLM-extracted)
  themes: Array<{name: string; prominence: "central" | "secondary" | "subtle"}>;
  mood: {primary: string[]; undertones: string[]; intensity: string};
  visual_style: {palette: string[]; composition: string[]; descriptors: string[]};
  narrative: {pacing: string; structure: string; tone: string};

  // Ground truth (manually curated)
  similar_to: SimilarityLink[];
}
```

### Relationship Types (Phase 1)

```typescript
type RelationType =
  | "visual_style"      // Share aesthetic qualities
  | "thematic"          // Share themes
  | "mood"              // Share emotional tone
  | "narrative_style"   // Similar storytelling
  | "creator"           // Same director/writer
  | "spiritual_successor"
  | "contrast"          // Different approaches to same theme
  | "audience_overlap"; // General "if you like X, you'll like Y"
```

Phase 2 will introduce free-form edges like: *"Both explore identity in dehumanizing systems, but BR2049 is melancholic where Severance is absurdist"*

---

## Test Queries (20)

| Category | Example |
|----------|---------|
| Similarity + Modifier | "Something like Severance but lighter" |
| Aesthetic/Style | "Movies with Blade Runner's visual style" |
| Thematic | "Stories about corporate dehumanization" |
| Creator-based | "Denis Villeneuve films and things that feel similar" |
| Mood-based | "Something unsettling but not horror" |

---

## Evaluation

### Metrics

| Metric | How to Measure |
|--------|----------------|
| **Relevance** | Do results match query intent? (1-5 scale) |
| **Explainability** | Does system explain WHY? Quality of explanation |
| **Surprise/Discovery** | Non-obvious but good results? |
| **Precision** | % of results actually relevant |

### Process

For each query × each system:
1. Run query
2. Record top 5 results
3. Score relevance (1-5)
4. Note explanation quality
5. Flag surprising discoveries or obvious misses

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                           │
│  - Run queries against all systems                          │
│  - Side-by-side results comparison                          │
│  - Capture evaluations                                       │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   FastAPI Backend                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │  Pure    │  │ Graphiti │  │  Open    │                   │
│  │  Vector  │  │  Agent   │  │ Memory   │                   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                   │
└───────┼─────────────┼─────────────┼───────────────────────────┘
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ Chroma  │   │ Neo4j   │   │ SQLite  │
   └─────────┘   │ Aura    │   └─────────┘
                 └─────────┘
```

### Common Interface

```python
class AgenticSystem(ABC):
    async def ingest(self, movies: List[Movie]) -> int
    async def query(self, query: str, limit: int = 5) -> AgentResponse
    async def health_check(self) -> bool
    async def clear(self) -> None

class AgentResponse(BaseModel):
    results: List[QueryResult]  # id, title, score, explanation
    reasoning: str              # How agent interpreted query
    system_context: str         # What context system provided
```

---

## Implementation Steps

1. **Dataset**: Curate 50 movies, fetch TMDB metadata, extract semantics via LLM, create ground truth links
2. **Systems**: Set up each system with unified interface
3. **Backend**: FastAPI with endpoints for each system
4. **Frontend**: React comparison UI with evaluation capture
5. **Evaluate**: Run queries, capture scores, document findings

---

## Success Criteria

Phase 1 is complete when:
- [ ] 50 movies with semantic data exist
- [ ] 3 systems queryable via unified interface
- [ ] 20 test queries evaluated across all systems
- [ ] Comparison UI shows results side-by-side
- [ ] Documented findings: which approach works best and why
- [ ] Decision made on Phase 2 architecture

---

## Decision: Mem0 Removed from Phase 1

**Date:** 2025-11-24
**Status:** Decided

### Problem

Mem0's LLM extraction (`infer=True`) rejected all movie descriptions, returning `{'results': []}` (NOOP).

**Tested:**
- Raw text: `memory.add(movie.to_text())` → empty
- Messages format: `memory.add([{role, content}])` → empty
- Fresh database (not deduplication) → empty

### Why It Failed

Mem0's LLM is **optimized for user conversations**, not static content:
- Expects: "I watched Severance and loved it" → extracts user preference
- Rejects: "Severance is a 2022 thriller..." → encyclopedic, not user memory

### With `infer=False`

Direct storage works, but bypasses all Mem0 features:
- No entity extraction
- No graph relationships (even with Neo4j)
- Just a ChromaDB wrapper → identical to Pure Vector

### Decision

**Remove Mem0 from Phase 1.** Can't test its capabilities without extraction.

**Phase 1:** Pure Vector, Graphiti, OpenMemory (3 systems)

**Phase 2+:** Use Mem0 for user interaction tracking where it excels.

### Lessons

1. Tool-problem fit matters more than popularity
2. Static content ≠ conversational memory
3. Test early before building full integration

---

## References

- [Mem0 Docs](https://docs.mem0.ai)
- [Graphiti GitHub](https://github.com/getzep/graphiti)
- [OpenMemory GitHub](https://github.com/CaviraOSS/OpenMemory)
- [ChromaDB Docs](https://docs.trychroma.com)
