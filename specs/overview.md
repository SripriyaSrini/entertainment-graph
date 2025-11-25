# The Entertainment Graph: Project Overview

## Vision

The Entertainment Graph is a knowledge graph that connects entertainment through meaningful relationships rather than isolated catalog entries. It enables **semantic navigation** beyond simple behavioral pattern matching.

Think of it as a map that shows how content connects—not through genres or tags, but through what they actually mean and how they make you feel.

These relationships are captured as **nodes and edges** that continuously evolve as new content emerges and culture shifts. The system uses **Graph RAG (Retrieval-Augmented Generation)**—combining the graph's structured semantic knowledge with LLM intelligence to navigate these relationships and generate personalized, explainable recommendations.

## Why a Graph?

Entertainment is fundamentally relational—the value lies in semantic connections, not isolated attributes. These multi-dimensional relationships can't be captured in simple similarity metrics or flat categories.

**Example**: Blade Runner 2049 and Dune share stark, monumental visuals—and that aesthetic connects to music videos with atmospheric electronic soundscapes, to nature documentaries on desert ecosystems, and to design shows exploring modernist architecture.

**Multi-hop reasoning**: Finding something "like Severance but lighter" means navigating through thematic and aesthetic edges while applying emotional tone filters.

**Explainability**: Every recommendation traces back through explicit edges. For example: "You connected with how The Office observes workplace dynamics with empathy. The Bear offers a similar lens—observing kitchen culture with the same compassion, in a dramatic register."

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Node** | A piece of content, creator, theme, mood, or context |
| **Edge** | A typed relationship with weight, confidence score, and provenance |
| **Traversal** | Multi-hop navigation through edges to discover connections |
| **Graph RAG** | LLM interprets query → generates graph traversal → retrieves subgraph → generates response |

## How Graph RAG Differs from Traditional RAG

**Traditional RAG:**
```
Query → Vector Search → Top Documents → LLM Context → Response
```

**Graph RAG:**
```
Query → LLM Understands Context → Generates Graph Query → Graph Traversal → Retrieves Subgraph → Augments LLM Context → Generates Experience
```

The key insight: graphs preserve relationships and enable multi-hop reasoning that vector search alone cannot provide.

## Project Goals

1. **Learning**: Understand graph databases, Graph RAG patterns, and Rust
2. **Spec-driven**: Document decisions before implementing
3. **Evaluate tools**: Research mem0, Graphiti, and similar technologies
4. **Build incrementally**: Start simple, evolve based on learnings

## Open Questions

- [ ] Which graph database/library to use?
- [ ] How to source entertainment data? (APIs, manual curation, etc.)
- [ ] What's the MVP scope? (Movies only? One user?)
- [ ] Rust for graph core, Python for LLM—or unified stack?

## Status

**Phase**: Research & Planning
