# ADR-001: Three-System Comparison Approach

**Date:** November 24, 2025
**Status:** Accepted
**Decision Makers:** Phase 1 Team

---

## Context

Before building our own Entertainment Graph system, we need to understand the tradeoffs between different retrieval paradigms. We initially planned to compare 4 systems but discovered one didn't fit our use case.

## Decision

**Compare these 3 systems for Phase 1:**

1. **Pure Vector (ChromaDB)** - Baseline: simple embedding similarity
2. **Graphiti (Neo4j)** - Graph-first with entity/relationship extraction
3. **OpenMemory** - Multi-sector memory decomposition

**Removed:**
4. ~~Mem0~~ - Doesn't work for static content (see [research/005-mem0-removal-decision.md](../../research/005-mem0-removal-decision.md))

## Rationale

### Why These 3 Systems?

**Pure Vector (Baseline)**
- ✅ Simplest approach - establishes baseline
- ✅ Fast, cheap, no infrastructure overhead
- ✅ Universal - works for any content type
- ❌ No structure - just semantic similarity

**Graphiti (Graph Structure)**
- ✅ Explicit relationships - fact-checkable
- ✅ Explainable - can show graph paths
- ✅ Temporal awareness - tracks when facts added
- ❌ Extraction overhead - LLM calls per movie
- ❌ Infrastructure - requires Neo4j

**OpenMemory (Cognitive Sectors)**
- ✅ Multi-sector decomposition - different memory types
- ✅ Hierarchical - sector-specific decay rates
- ✅ Novel approach - cognitive architecture
- ❌ Less mature - newer project
- ❌ Documentation gaps

### Why These Represent Different Paradigms?

| Paradigm | System | Key Difference |
|----------|--------|----------------|
| **Flat embedding space** | Pure Vector | Single vector per movie, no structure |
| **Graph relationships** | Graphiti | Explicit edges between entities |
| **Cognitive decomposition** | OpenMemory | Multi-sector storage (semantic, emotional, procedural) |

Each represents a fundamentally different way to organize and retrieve information.

## Alternatives Considered

### 4-System Comparison (Rejected)
**Option:** Include Mem0 as 4th system
**Why rejected:** Mem0's LLM extraction optimized for user conversations, not static content. All ingestion attempts returned empty. With `infer=False`, it's just a ChromaDB wrapper (identical to Pure Vector).
**Details:** See [research/005-mem0-removal-decision.md](../../research/005-mem0-removal-decision.md)

### 2-System Comparison (Rejected)
**Option:** Just Pure Vector vs Graphiti
**Why rejected:** Missing the "cognitive sectors" paradigm. OpenMemory adds a third distinct approach worth evaluating.

### Traditional Graph (Rejected)
**Option:** Manual graph construction (Neo4j only, no Graphiti)
**Why rejected:** Phase 1 goal is to compare *systems*, not build from scratch. Graphiti provides automatic extraction + temporal features.

## Consequences

### Positive
- ✅ Clear comparison of 3 distinct paradigms
- ✅ Manageable scope (3 systems implementable in Phase 1)
- ✅ Each system represents real-world production approach
- ✅ Findings will inform Phase 2 hybrid architecture

### Negative
- ⚠️ Missing user-memory paradigm (Mem0) - but that's Phase 2 scope anyway
- ⚠️ Can't evaluate 4th dimension (user preferences) in Phase 1
- ⚠️ OpenMemory less mature - potential API instability

### Neutral
- Phase 1 focuses on static content retrieval (appropriate)
- User tracking deferred to Phase 2 (appropriate)

## Validation

We'll know this was the right decision if:
- [ ] Each system shows distinct strengths/weaknesses
- [ ] Results inform Phase 2 architecture choices
- [ ] No system is universally best (confirms need for comparison)
- [ ] Findings lead to hybrid approach in Phase 2

## Related Decisions
- [ADR-002: Agentic Retrieval Approach](ADR-002-agentic-retrieval.md)
- [Mem0 Removal Investigation](../../research/005-mem0-removal-decision.md)

## References
- Phase 1 spec: [specs/phase1.md](../phase1.md)
- Research notes: [research/001-mem0.md](../../research/001-mem0.md), [002-graphiti.md](../../research/002-graphiti.md), [003-openmemory.md](../../research/003-openmemory.md), [004-pure-vector.md](../../research/004-pure-vector.md)
