# Specifications & Design Documentation

This directory contains all design specifications, architecture decisions, and system documentation for the Entertainment Graph project.

---

## Directory Structure

```
specs/
├── README.md                           # This file
├── phase1.md                           # Phase 1 overall plan & goals
├── overview.md                         # Project overview
├── systems/                            # System design specifications
│   ├── pure_vector.md                  # Pure Vector (ChromaDB) design
│   ├── graphiti.md                     # Graphiti (Neo4j) design
│   └── openmemory.md                   # OpenMemory design
└── decisions/                          # Architecture Decision Records (ADRs)
    ├── ADR-001-system-selection.md     # Why these 3 systems?
    └── ADR-002-agentic-retrieval.md    # Why LLM-in-loop?
```

---

## Document Types

### 1. Phase Plans (`phase1.md`)
**Purpose:** High-level goals, scope, success criteria for each phase

**Contents:**
- What we're building and why
- Comparison approach
- Dataset design
- Success criteria
- Infrastructure decisions

**When to read:** Start here to understand the project's direction

---

### 2. System Designs (`systems/*.md`)
**Purpose:** Detailed specifications for each retrieval system

**Contents:**
- Architecture & components
- Storage strategy
- Retrieval approach
- Strengths & weaknesses
- Cost & performance analysis
- Implementation details

**Format:**
- **Overview:** What this system is
- **Architecture:** How it's built
- **Storage Strategy:** How data is ingested
- **Retrieval Strategy:** How queries work
- **Strengths/Weaknesses:** When to use this system
- **Comparison:** vs other systems
- **Implementation:** Code structure, files, configuration
- **Test Queries:** Expected behavior
- **Status:** Current state

**When to read:**
- Before implementing a system
- When deciding which system to use
- When debugging system behavior

---

### 3. Architecture Decision Records (`decisions/ADR-*.md`)
**Purpose:** Document key architectural decisions and their rationale

**Format (standard ADR):**
- **Context:** What decision needed to be made?
- **Decision:** What did we choose?
- **Rationale:** Why this choice?
- **Alternatives Considered:** What else did we evaluate?
- **Consequences:** What are the tradeoffs?
- **Validation:** How will we know this was right?

**Naming:** `ADR-XXX-short-description.md`

**When to read:**
- To understand why the system is built this way
- When revisiting past decisions
- When proposing changes to architecture

**When to write:**
- Major architectural choices
- Technology selection
- Significant tradeoffs
- "Why didn't we do X?" questions

---

## Spec-Driven Development Workflow

This project follows a **spec-driven development** approach:

### 1. **Design First** → Write specs before code
- Document the architecture
- Define interfaces
- Identify components
- Plan implementation

### 2. **Implement** → Build according to specs
- Follow system designs
- Reference ADRs for decisions
- Update specs if design changes

### 3. **Validate** → Verify against specs
- Check acceptance criteria
- Compare behavior to design
- Document deviations

### 4. **Document** → Update specs with learnings
- Add findings to system designs
- Create ADRs for new decisions
- Keep specs in sync with code

---

## How to Navigate

### "I want to understand the overall project"
→ Read [phase1.md](phase1.md)

### "I want to know how Pure Vector works"
→ Read [systems/pure_vector.md](systems/pure_vector.md)

### "I want to know why we chose these 3 systems"
→ Read [decisions/ADR-001-system-selection.md](decisions/ADR-001-system-selection.md)

### "I want to know why we use LLM reasoning"
→ Read [decisions/ADR-002-agentic-retrieval.md](decisions/ADR-002-agentic-retrieval.md)

### "I want to compare the 3 systems"
→ Read all files in [systems/](systems/), focus on Strengths/Weaknesses sections

### "I want to implement a new system"
1. Read existing system designs for patterns
2. Create new `systems/new-system.md` with same structure
3. Implement following the spec
4. Update spec with actual behavior

---

## Spec Maintenance

### When to Update Specs

✅ **Always update when:**
- Architecture changes
- New system added
- Major decision made
- Implementation deviates from design

❌ **Don't update for:**
- Minor code refactors (same behavior)
- Bug fixes (unless design was wrong)
- Performance tweaks (unless fundamental approach changes)

### Keeping Specs Current

**Before writing code:**
- Check if spec exists
- Update spec if needed
- Get alignment on design

**After implementation:**
- Verify behavior matches spec
- Document any deviations
- Add learnings (actual performance, issues found)

---

## ADR Numbering

ADRs use sequential numbering: `ADR-001`, `ADR-002`, etc.

**Current ADRs:**
- ADR-001: System Selection (why 3 systems)
- ADR-002: Agentic Retrieval (why LLM-in-loop)

**Next ADR:** ADR-003

---

## Spec Template

When creating new system designs, follow this structure:

```markdown
# [System Name] Design

**Date:** YYYY-MM-DD
**Status:** [Planned | In Progress | Implemented]

## Overview
Brief description

## Architecture
Components and how they connect

## Storage Strategy
How data is ingested

## Retrieval Strategy
How queries work

## Strengths
What this system is good at

## Weaknesses
What this system struggles with

## Comparison to Other Systems
vs Pure Vector, vs Graphiti, etc.

## Implementation Details
File locations, key methods, configuration

## Test Queries & Expected Behavior
Example queries and what should happen

## Cost Analysis
Ingestion + query costs

## Performance Characteristics
Speed, scalability, bottlenecks

## Status
Current state and next steps
```

---

## Related Documentation

- **Implementation:** `/python/src/entertainment_graph/systems/`
- **Tests:** `/python/test_*.py`, `/python/compare_systems.py`
- **Task Tracking:** `/TASKS.md`
- **Progress Summary:** `/PROGRESS.md`
- **Comparison Results:** `/COMPARISON_RESULTS.md`

---

## Questions?

If you have questions about:
- **Project direction** → See [phase1.md](phase1.md)
- **System design** → See [systems/](systems/)
- **Why we made a decision** → See [decisions/](decisions/)
- **How to implement** → See system design + code

For questions not answered in specs, file an issue or update the relevant spec.
