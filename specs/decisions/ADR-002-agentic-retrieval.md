# ADR-002: Agentic Retrieval (LLM-in-Loop)

**Date:** November 24, 2025
**Status:** Accepted
**Decision Makers:** Phase 1 Team

---

## Context

We need to decide whether to compare systems using **raw retrieval** (just return documents) or **agentic retrieval** (LLM reasons over results).

Traditional RAG: `Query → Retrieve → Return Top K`
Agentic RAG: `Query → Retrieve → LLM Reasons → Explained Results`

## Decision

**Use agentic retrieval for all systems.**

All 3 systems include an LLM reasoning step after retrieval:
1. Retrieve context from system (vectors, graph, sectors)
2. LLM interprets query + context
3. LLM explains why each result matches
4. Return ranked results with explanations

## Rationale

### Why Agentic vs Raw Retrieval?

**Agentic retrieval advantages:**
- ✅ **Explainability**: Users understand *why* a movie was recommended
- ✅ **Reasoning**: LLM can interpret nuanced queries ("something like X but lighter")
- ✅ **Fair comparison**: Each system provides context to LLM; LLM quality is constant
- ✅ **Real-world use case**: Production systems need explanations, not just scores

**Raw retrieval problems:**
- ❌ No explanations - just similarity scores
- ❌ Can't interpret complex queries - relies purely on embedding similarity
- ❌ Harder to compare - Pure Vector score 0.8 ≠ Graphiti score 0.8

### What Each System Provides to LLM

| System | Context Provided | LLM Task |
|--------|-----------------|----------|
| **Pure Vector** | Similar documents (text chunks) | "Explain why these movies match the query" |
| **Graphiti** | Graph nodes, edges, relationships | "Explain matches using graph structure" |
| **OpenMemory** | Memories from cognitive sectors | "Explain matches using sector information" |

The LLM **does not** do the retrieval - it explains what the system found.

## Alternatives Considered

### Raw Retrieval Only (Rejected)
**Option:** Just return top K results with scores, no LLM
```python
results = chroma.query(query_embedding, n_results=5)
return results  # Just IDs and scores
```

**Why rejected:**
- No explainability
- Can't handle complex queries ("lighter", "more philosophical")
- Scores not comparable across systems
- Not production-ready (users need explanations)

### LLM Does Retrieval (Rejected)
**Option:** LLM generates search queries, does filtering
```python
search_queries = llm.generate_queries(user_query)
results = system.search(search_queries)
return llm.filter_and_rank(results)
```

**Why rejected:**
- Mixes system capabilities with LLM capabilities
- Can't isolate what the *system* contributed
- Defeats purpose of comparing retrieval systems
- LLM could compensate for weak retrieval

### Hybrid: Some Agentic, Some Raw (Rejected)
**Option:** Pure Vector gets LLM, others don't
**Why rejected:** Unfair comparison - some systems get reasoning boost, others don't

## Consequences

### Positive
- ✅ All systems provide explainable results
- ✅ Fair comparison - LLM quality is constant across systems
- ✅ Can evaluate system-specific strengths (graph structure, sectors, etc.)
- ✅ Production-ready pattern (users need explanations)
- ✅ Enables complex queries ("like X but lighter")

### Negative
- ⚠️ LLM adds cost (~$0.01 per query)
- ⚠️ LLM adds latency (1-2 seconds)
- ⚠️ Can't isolate pure retrieval quality (LLM may "fix" bad retrieval)

### Mitigation
- Use same LLM (GPT-4) for all systems → fair comparison
- Measure retrieval quality by looking at *what context was provided* to LLM
- Explicit prompt: "Explain based on context provided" (no external knowledge)

## Implementation

### Common Pattern
```python
class AgenticSystem(ABC):
    async def query(self, query: str, limit: int = 5) -> AgentResponse:
        # 1. System-specific retrieval
        context = self._retrieve_context(query, limit)

        # 2. LLM reasoning (same for all systems)
        llm_response = self.openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Explain matches based on context..."},
                {"role": "user", "content": f"Query: {query}\nContext: {context}"}
            ]
        )

        # 3. Return explained results
        return AgentResponse(results=..., reasoning=llm_response)
```

### System-Specific Context

**Pure Vector:**
```
Context: [
  "Severance (2022) - Explores corporate control, psychological thriller...",
  "Blade Runner 2049 (2017) - Dystopian future, replicants, identity...",
]
```

**Graphiti:**
```
Context: [
  "Severance -[EXPLORES_THEME]-> corporate control",
  "Severance -[HAS_MOOD]-> unsettling",
  "Blade Runner 2049 -[EXPLORES_THEME]-> identity",
]
```

**OpenMemory:**
```
Context: [
  "Severance (semantic sector): psychological thriller about corporate control",
  "Severance (emotional sector): unsettling, clinical mood",
  "Severance (procedural sector): slow-burn pacing",
]
```

## Validation

We'll know this was the right decision if:
- [ ] All systems return explainable results
- [ ] LLM explanations reference system-specific context (graph edges, sectors)
- [ ] Complex queries work ("like X but lighter")
- [ ] Users can understand *why* a recommendation was made

## Related Decisions
- [ADR-001: System Selection](ADR-001-system-selection.md)

## References
- Phase 1 spec: [specs/phase1.md](../phase1.md)
- System designs: [specs/systems/](../systems/)
