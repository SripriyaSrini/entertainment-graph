# Phase 1 Tasks - System Comparison

**Date Started:** November 23, 2025
**Phase Goal:** Compare 3 retrieval systems empirically before building Phase 2 hybrid architecture
**Status:** 🔄 In Progress (OpenMemory integration ongoing)

---

## Task Status Legend

- ✅ Completed
- 🔄 In Progress
- ⏳ Pending
- ⏸️ Blocked

---

## Phase 1 Overview

### Systems to Compare
1. ✅ **Pure Vector** (ChromaDB) - Baseline: simple embedding similarity
2. ✅ **Graphiti** (Neo4j) - Graph-first with entity/relationship extraction
3. 🔄 **OpenMemory** - Multi-sector memory decomposition

### Key Decisions
- [ADR-001: System Selection](specs/decisions/ADR-001-system-selection.md) - Why these 3 systems?
- [ADR-002: Agentic Retrieval](specs/decisions/ADR-002-agentic-retrieval.md) - Why LLM-in-loop?

---

## System 1: Pure Vector (ChromaDB)

**Status:** ✅ Complete
**Implementation Date:** November 23-24, 2025
**Approach:** Implemented before formal task tracking (organic development)

### Files Created
- ✅ [python/src/entertainment_graph/systems/pure_vector.py](python/src/entertainment_graph/systems/pure_vector.py)
- ✅ [specs/systems/pure_vector.md](specs/systems/pure_vector.md)
- ✅ [python/test_basic.py](python/test_basic.py)

### Key Features
- Single embedding per movie (OpenAI text-embedding-3-small)
- ChromaDB local storage
- LLM reasoning over retrieved results
- Cost: ~$0.03 for 5 movies + 3 queries

### Findings
- ✅ Fast ingestion (~1 sec per movie)
- ✅ Good semantic similarity
- ❌ False positive: returned "Her" for "Denis Villeneuve movies" (wrong director)
- ✅ Wide recall (3 results per query)

**Reference:** [specs/systems/pure_vector.md](specs/systems/pure_vector.md)

---

## System 2: Graphiti (Neo4j)

**Status:** ✅ Complete
**Implementation Date:** November 24, 2025
**Approach:** Implemented before formal task tracking

### Files Created
- ✅ [python/src/entertainment_graph/systems/graphiti_system.py](python/src/entertainment_graph/systems/graphiti_system.py)
- ✅ [specs/systems/graphiti.md](specs/systems/graphiti.md)
- ✅ [python/test_graphiti.py](python/test_graphiti.py)

### Key Features
- Automatic entity/relationship extraction via LLM
- Neo4j Aura (cloud) storage
- Hybrid retrieval: semantic + BM25 + graph traversal
- Temporal awareness (tracks when facts added)
- Cost: ~$0.13 for 5 movies + 3 queries (4x Pure Vector)

### Findings
- ✅ 100% factual accuracy on director query (used `DIRECTED_BY` relationship)
- ✅ Explainable via graph paths
- ❌ Lower recall (1-2 results per query)
- ⚠️ Slow ingestion (~5-10 sec per movie due to LLM extraction)

**Reference:** [specs/systems/graphiti.md](specs/systems/graphiti.md)

---

## System 3: OpenMemory (Multi-Sector)

**Status:** 🔄 In Progress
**Implementation Date:** November 25, 2025 (ongoing)
**Approach:** Spec-driven development (documented task breakdown below)

### Overview
Multi-sector memory decomposition with cognitive architecture:
- **Semantic sector:** Facts, themes, genres (decay: 0.001)
- **Emotional sector:** Mood, visual style, tone (decay: 0.01)
- **Procedural sector:** Pacing, structure, patterns (decay: 0.002)

Each movie stored as 3 memories across sectors.

**Design:** [specs/systems/openmemory.md](specs/systems/openmemory.md)

---

### ✅ TASK OM-1: Add OpenMemory Python SDK Dependency
**Status:** ✅ Completed (2025-11-25)

**Changes:**
- Modified: [python/pyproject.toml](python/pyproject.toml)
- Added `openmemory-py>=0.1.0` to dependencies

**Verification:**
```bash
python -c "from openmemory import OpenMemory; print('✓')"
# ✓ OpenMemory import successful
```

---

### ✅ TASK OM-2: Design Memory Sector Classification Strategy
**Status:** ✅ Completed (2025-11-25)

**Changes:**
- Created: [specs/systems/openmemory.md](specs/systems/openmemory.md)

**Design Summary:**
- Semantic: Facts, themes, plot
- Emotional: Mood, visual style, tone
- Procedural: Pacing, structure, similarity

---

### ✅ TASK OM-3-6: Implement OpenMemorySystem
**Status:** ✅ Completed (2025-11-25)

**Changes:**
- Created: [python/src/entertainment_graph/systems/openmemory_system.py](python/src/entertainment_graph/systems/openmemory_system.py)

**Implemented:**
- Core structure following `AgenticSystem` interface
- Multi-sector ingestion (3 memories per movie)
- Query with sector classification + LLM reasoning
- Health check and clear methods

---

### ✅ TASK OM-7: Update System Registry
**Status:** ✅ Completed (2025-11-25)

**Changes:**
- Modified: [python/src/entertainment_graph/systems/__init__.py](python/src/entertainment_graph/systems/__init__.py)
- Modified: [python/src/entertainment_graph/main.py](python/src/entertainment_graph/main.py)

**Result:**
- OpenMemorySystem exported and registered
- FastAPI endpoints available

---

### ✅ TASK OM-8: Add to Comparison Script
**Status:** ✅ Completed (2025-11-25)

**Changes:**
- Modified: [python/compare_systems.py](python/compare_systems.py)

**Result:**
- Three-way comparison: Pure Vector vs Graphiti vs OpenMemory
- Side-by-side output for all queries

---

### ✅ TASK OM-9: Test End-to-End Integration
**Status:** ✅ Completed (2025-11-25)

**Test Plan:**
1. ✅ Systems initialized
2. ✅ Ingest 5 movies into all 3 systems
3. ✅ Query with 3 test cases
4. ✅ Analyze results

**API Fixes Applied:**
- ✅ Fixed: `create_single_waypoint` → `_add_async` (async context)
- ✅ Fixed: `hsg_query` → `_query_async` (async context)
- ✅ Fixed: `sector` parameter → `tags` parameter (sectors tracked via tags)
- ✅ Updated query filters to use `filters={"tags": [sector]}`
- ✅ Fixed: Async event loop conflict (use `_add_async` / `_query_async` instead of `add` / `query`)
- ✅ Fixed: Metadata extraction - parse JSON strings from `result.get("meta", "{}")`
- ✅ Fixed: Tags extraction - parse JSON strings from `result.get("tags", "[]")`
- ✅ Fixed: Score field - use `result.get("score", 0.0)` instead of "similarity"

**Final Test Results:**
- ✅ All 3 systems fully functional
- ✅ Ingestion successful: 5 movies × 3 sectors = 15 memories stored
- ✅ Query successful: All 3 queries returned results with sector-specific explanations
- ✅ OpenMemory successfully using semantic, emotional, and procedural sectors

**Key Findings:**
- **Query 1 (Dystopian corporate)**: OpenMemory identified both Severance and Blade Runner 2049, with sector-based explanations
- **Query 2 (Visual style)**: OpenMemory retrieved Blade Runner 2049 from emotional sector (visual palette) and procedural sector
- **Query 3 (Director)**: OpenMemory correctly identified both Denis Villeneuve films using semantic sector

---

### 🔄 TASK OM-10: Document Findings
**Status:** 🔄 In Progress
**Depends On:** TASK OM-9 ✅

**To Update:**
- 🔄 [PHASE1_TASKS.md](PHASE1_TASKS.md) - Mark TASK OM-9 complete with final results
- ⏳ [PROGRESS.md](PROGRESS.md) - Mark OpenMemory complete (3/3 systems)
- ⏳ [COMPARISON_RESULTS.md](COMPARISON_RESULTS.md) - Add OpenMemory results
- ⏳ Update comparison table with 3-way analysis

---

## Phase 1 Completion Tasks

### ⏳ TASK P1-1: Evaluate Comparison Results
**Status:** ⏳ Pending
**Depends On:** All systems complete

**Activities:**
- Analyze precision/recall for each system
- Document cost vs performance tradeoffs
- Identify strengths/weaknesses per query type
- Determine which system for which use case

**Deliverable:** Updated [COMPARISON_RESULTS.md](COMPARISON_RESULTS.md)

---

### ⏳ TASK P1-2: Make Phase 2 Architecture Decision
**Status:** ⏳ Pending
**Depends On:** P1-1

**Decision:**
- Hybrid approach? (combine systems)
- Single system winner?
- Custom solution based on learnings?

**Deliverable:** ADR-003: Phase 2 Architecture Decision

---

### ⏳ TASK P1-3: Document Spec-Driven Workflow
**Status:** ⏳ Pending

**Activities:**
- Document the spec-driven development process used for OpenMemory
- Create workflow guide for Phase 2
- Compare informal (Pure Vector/Graphiti) vs formal (OpenMemory) approaches

**Deliverable:** Blog post or documentation showing evolution

---

## Progress Summary

### Overall Phase 1
- **Systems:** 2/3 complete, 1 in progress (90%)
- **Comparison:** Pending final results
- **Documentation:** Ongoing

### System Completion
| System | Status | Date | Files |
|--------|--------|------|-------|
| Pure Vector | ✅ Complete | Nov 23-24 | pure_vector.py, test_basic.py |
| Graphiti | ✅ Complete | Nov 24 | graphiti_system.py, test_graphiti.py |
| OpenMemory | 🔄 Testing | Nov 25 | openmemory_system.py, compare_systems.py |

### OpenMemory Tasks
- **Completed:** 8/10 tasks (80%)
- **In Progress:** 1/10 tasks (10%)
- **Pending:** 1/10 tasks (10%)

---

## Git Commits

### Completed (Pure Vector)
- ✅ `feat: implement Pure Vector baseline system`
- ✅ `test: add basic Pure Vector test`
- ✅ `docs: add Pure Vector design spec`

### Completed (Graphiti)
- ✅ `feat: implement Graphiti system with Neo4j`
- ✅ `test: add Graphiti integration test`
- ✅ `docs: add Graphiti design spec`

### Completed (OpenMemory)
- ✅ `feat: add openmemory-py dependency`
- ✅ `docs: add OpenMemory design spec`
- ✅ `feat: implement OpenMemorySystem with multi-sector storage`
- ✅ `feat: register OpenMemory in system registry`
- ✅ `feat: add OpenMemory to comparison script`

### Completed (Documentation)
- ✅ `docs: reorganize specs folder (systems/, decisions/)`
- ✅ `docs: add ADR-001 system selection`
- ✅ `docs: add ADR-002 agentic retrieval`
- ✅ `docs: add specs README with navigation guide`
- ✅ `refactor: remove /research folder (moved to specs)`

### Pending
- ⏳ `test: complete three-way comparison`
- ⏳ `docs: update COMPARISON_RESULTS with OpenMemory findings`
- ⏳ `docs: finalize Phase 1 summary`

---

## Key Learnings (So Far)

### Pure Vector vs Graphiti
- **Precision:** Graphiti wins (100% vs 67% on factual queries)
- **Recall:** Pure Vector wins (3 vs 1-2 results)
- **Cost:** Pure Vector wins ($0.03 vs $0.13)
- **Speed:** Pure Vector wins (1 sec vs 5-10 sec ingestion)
- **Explainability:** Graphiti wins (graph paths vs semantic similarity)

### Spec-Driven Development
- OpenMemory implemented with formal task tracking
- Clear acceptance criteria → easier validation
- Design docs before code → fewer API mismatches
- Task breakdown → predictable progress

---

## Next Steps

1. ✅ Fix OpenMemory API issues
2. 🔄 Complete three-way comparison test
3. ⏳ Analyze OpenMemory results
4. ⏳ Update COMPARISON_RESULTS.md
5. ⏳ Decide Phase 2 architecture
6. ⏳ Write Phase 1 retrospective

---

## References

- **Specs:** [specs/](specs/)
  - [phase1.md](specs/phase1.md) - Overall plan
  - [systems/](specs/systems/) - System designs
  - [decisions/](specs/decisions/) - ADRs
- **Implementation:** [python/src/entertainment_graph/systems/](python/src/entertainment_graph/systems/)
- **Tests:** [python/test_*.py](python/), [python/compare_systems.py](python/compare_systems.py)
- **Results:** [COMPARISON_RESULTS.md](COMPARISON_RESULTS.md), [PROGRESS.md](PROGRESS.md)
