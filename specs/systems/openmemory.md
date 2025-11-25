# OpenMemory System Design

**Date:** November 24, 2025
**Status:** Design specification for OpenMemory integration

---

## Overview

OpenMemory uses hierarchical memory decomposition with 5 cognitive sectors. For entertainment discovery, we'll map movie attributes to appropriate sectors.

---

## Memory Sector Classification Strategy

### Sectors Used for Static Movie Content

**1. Semantic Sector**
- **Purpose:** Facts, themes, conceptual knowledge
- **Movie attributes:**
  - Title, year, director, cast
  - Genres
  - Themes (with prominence: central/secondary/subtle)
  - Plot summary
  - Narrative structure (linear/non-linear/etc)
- **Decay rate:** 0.001 (low decay - facts don't change)
- **Example memory:**
  ```
  "Blade Runner 2049 (2017) directed by Denis Villeneuve.
  Explores central theme of identity and what it means to be human,
  secondary theme of environmental collapse, subtle theme of memory and mortality.
  Genres: Science Fiction, Neo-noir."
  ```

**2. Emotional Sector**
- **Purpose:** Mood, aesthetics, feeling-based attributes
- **Movie attributes:**
  - Mood (primary moods, undertones, intensity)
  - Visual style (palette, composition, descriptors)
  - Emotional arc
  - Tone (somber/playful/etc)
- **Decay rate:** 0.01 (high decay - emotions fade faster)
- **Example memory:**
  ```
  "Blade Runner 2049 evokes contemplative and melancholic mood with hopeful undertones.
  Visual palette: orange haze, neon blues, stark grays, desaturated earth tones.
  Visual style: sweeping wide shots, minimalist composition, stark lighting contrasts.
  Intensity: moderate."
  ```

**3. Procedural Sector**
- **Purpose:** Patterns, processes, "how things work"
- **Movie attributes:**
  - Narrative pacing (slow-burn/frenetic/etc)
  - Perspective (third-person/first-person/etc)
  - Runtime
  - Similar-to relationships (how similarity works)
- **Decay rate:** 0.002 (medium decay)
- **Example memory:**
  ```
  "Blade Runner 2049 uses slow-burn pacing with deliberate, contemplative structure.
  Runtime: 164 minutes. Similar to original Blade Runner due to visual_style:
  shares neo-noir aesthetic, dystopian atmosphere, philosophical depth."
  ```

### Sectors NOT Used (Static Content)

**4. Episodic Sector**
- **Purpose:** Time-based events, user interactions
- **NOT used for:** Static movie data (no temporal events to track)
- **Future use:** Could track user watch history, discovery timestamps

**5. Reflective Sector**
- **Purpose:** Meta-knowledge, self-reflection, patterns about patterns
- **NOT used for:** Static movie data
- **Future use:** Could track user preference patterns, recommendation effectiveness

---

## Ingestion Strategy

### Multi-Sector Storage

Each movie will be stored as **3 memories** (one per active sector):

1. **Semantic memory:** Facts + themes + structure
2. **Emotional memory:** Mood + visual style + tone
3. **Procedural memory:** Pacing + perspective + similarity patterns

### Memory Creation Flow

```python
async def ingest(movies: list[Movie]) -> int:
    for movie in movies:
        # Create 3 memories per movie
        semantic_memory = _create_semantic_memory(movie)
        emotional_memory = _create_emotional_memory(movie)
        procedural_memory = _create_procedural_memory(movie)

        # Store with sector-specific waypoints
        await openmemory.create_single_waypoint(
            content=semantic_memory,
            sector="semantic",
            metadata={"movie_id": movie.id, "title": movie.title}
        )
        # ... repeat for emotional and procedural
```

---

## Query Strategy

### Multi-Sector Retrieval

Query process:
1. **Classify query intent** (LLM determines which sectors to search)
2. **Search relevant sectors** (semantic for facts, emotional for vibes, etc.)
3. **Aggregate results** across sectors
4. **LLM reasoning** to explain why movies match

### Example Query Routing

**Query:** "Denis Villeneuve movies"
- **Sectors:** Semantic only (factual query)
- **Search:** `openmemory.hsg_query("Denis Villeneuve", sectors=["semantic"])`

**Query:** "Films with melancholic, contemplative mood"
- **Sectors:** Emotional + Semantic
- **Search:** Multi-sector query, weight emotional matches higher

**Query:** "Slow-burn sci-fi with philosophical themes"
- **Sectors:** All 3 (semantic for themes/genre, emotional for mood, procedural for pacing)
- **Search:** Cross-sector aggregation

---

## Integration Points

### Files to Create
- `python/src/entertainment_graph/systems/openmemory_system.py`

### Files to Modify
- `python/src/entertainment_graph/systems/__init__.py` (export OpenMemorySystem)
- `python/src/entertainment_graph/main.py` (register system)
- `python/compare_systems.py` (add to comparison)

### Configuration
- OpenMemory uses local SQLite by default (no additional config needed)
- Optional: Add `OPENMEMORY_DB_PATH` to `.env` for custom location

---

## Expected Behavior

### Compared to Other Systems

**vs Pure Vector:**
- OpenMemory: Multi-sector decomposition may improve retrieval precision
- Pure Vector: Single embedding space, simpler but less structured

**vs Graphiti:**
- OpenMemory: Automatic sector classification (no manual relationship extraction)
- Graphiti: Explicit graph relationships, requires LLM extraction

### Success Metrics

Test queries to validate:
1. **Factual query:** "Denis Villeneuve movies" (should match semantic sector)
2. **Mood query:** "Contemplative, melancholic films" (should match emotional sector)
3. **Pacing query:** "Slow-burn narratives" (should match procedural sector)
4. **Multi-sector:** "Slow-burn sci-fi about identity" (all 3 sectors)

Compare precision/recall vs Pure Vector and Graphiti.

---

## Implementation Notes

### Memory Content Format

Keep memories human-readable and semantically rich:
- ✓ "Explores central theme of identity"
- ✗ "Theme: identity, prominence: central"

### Sector Selection Logic

Use LLM-based classification for query routing:
```python
def _classify_query(query: str) -> list[str]:
    # LLM determines: factual? emotional? pacing-related?
    # Returns: ["semantic"] or ["emotional", "semantic"] etc.
```

### Handling Similar-to Relationships

Store bidirectional relationships in procedural sector:
```
"Blade Runner 2049 is similar to original Blade Runner
due to visual_style (neo-noir aesthetic, dystopian atmosphere).
Also similar to Dune due to creator (same director Denis Villeneuve)."
```

---

## Next Steps

1. ✓ Design complete
2. Implement `OpenMemorySystem` class following `AgenticSystem` interface
3. Test with 5 sample movies
4. Add to comparison script
5. Evaluate vs Pure Vector and Graphiti
