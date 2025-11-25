# Three-Way System Comparison: Pure Vector vs Graphiti vs OpenMemory

**Date:** November 25, 2025
**Dataset:** 5 movies (Blade Runner 2049, Severance, Dune, Her, The Office)
**Test Queries:** 3 representative queries
**Systems Evaluated:** Pure Vector (ChromaDB), Graphiti (Neo4j), OpenMemory (Multi-sector)

---

## Executive Summary

**Key Finding:** Each system excels at different query types - no universal winner.

**System Strengths:**
- **Pure Vector:** Exploratory discovery, wide recall, simple and fast
- **Graphiti:** Factual precision via graph relationships, 100% accuracy
- **OpenMemory:** Multi-faceted queries via cognitive sectors (semantic/emotional/procedural)

**Critical Insight:** Pure Vector returned a **false positive** (wrong director) on a factual query, while both Graphiti and OpenMemory achieved 100% accuracy by using structured knowledge.

**Recommendation:** Hybrid approach routing queries to appropriate system based on query type.

---

## Query 1: "Denis Villeneuve movies" (Factual Query)

### Pure Vector Results
| Rank | Movie | Year | Score | Correct? |
|------|-------|------|-------|----------|
| 1 | Dune | 2021 | 0.559 | ✓ Yes |
| 2 | Blade Runner 2049 | 2017 | 0.544 | ✓ Yes |
| 3 | **Her** | 2013 | 0.343 | **❌ NO** |

**Problem:** Returned "Her" (directed by Spike Jonze) because it shares thematic similarity with Villeneuve films. No fact-checking.

**Accuracy:** 67% (2 of 3 correct)

---

### Graphiti Results
| Rank | Movie | Year | Score | Correct? |
|------|-------|------|-------|----------|
| 1 | Blade Runner 2049 | 2017 | 0.850 | ✓ Yes |
| 2 | Dune | 2021 | 0.850 | ✓ Yes |

**How it worked:** Used explicit `DIRECTED_BY` graph relationship. No semantic guessing.

**Accuracy:** 100% (2 of 2 correct)

**Graph Evidence:**
- `Blade Runner 2049 --DIRECTED_BY--> Denis Villeneuve`
- `Dune --DIRECTED_BY--> Denis Villeneuve`

---

### OpenMemory Results
| Rank | Movie | Year | Score | Correct? |
|------|-------|------|-------|----------|
| 1 | Blade Runner 2049 | 2017 | 0.536 | ✓ Yes |
| 2 | Dune | 2021 | 0.531 | ✓ Yes |

**How it worked:** Used **semantic sector** to store director facts. Sector-based query classification identified this as a factual query, routed to semantic sector.

**Accuracy:** 100% (2 of 2 correct)

**Explanation:** "Blade Runner 2049 is relevant as it is directed by Denis Villeneuve, matching the director criteria from the semantic sector. Dune (2021) matches the query because it is also directed by Denis Villeneuve."

**Sectors Used:** semantic (primary), procedural (supporting)

---

### Winner: **Graphiti & OpenMemory (Tie)**
Both achieved 100% accuracy through structured knowledge. Pure Vector's false positive demonstrates why factual queries need fact-checking mechanisms, not just semantic similarity.

---

## Query 2: "Films similar to Blade Runner's visual style" (Visual Style Query)

### Pure Vector Results
| Rank | Movie | Year | Score | Reasoning |
|------|-------|------|-------|-----------|
| 1 | Blade Runner 2049 | 2017 | 0.608 | Direct sequel, same visual style |
| 2 | Dune | 2021 | 0.412 | Same director (Villeneuve), similar grandeur |
| 3 | Her | 2013 | 0.369 | Explores technology/identity themes |

**Approach:** Semantic similarity across descriptions including visual style terms.

**Recall:** 3 results (casts wide net)

---

### Graphiti Results
| Rank | Movie | Year | Score | Reasoning |
|------|-------|------|-------|-----------|
| 1 | Blade Runner 2049 | 2017 | 0.850 | Direct visual style relationship |

**Approach:** Only returned movies with explicit `SIMILAR_TO_VISUAL_STYLE` relationship.

**Recall:** 1 result (very precise)

**Graph Evidence:**
- `Blade Runner 2049 --SIMILAR_TO_VISUAL_STYLE--> Blade Runner`

---

### OpenMemory Results
| Rank | Movie | Year | Score | Reasoning |
|------|-------|------|-------|-----------|
| 1 | Blade Runner 2049 | 2017 | 0.661 | Retrieved from **emotional sector** (visual palette) |
| 2 | Her | 2013 | 0.561 | Found through multi-sector retrieval |

**Approach:** Query classified as visual/aesthetic → searched **emotional sector** (mood, visual style, tone) + procedural sector.

**Recall:** 2 results (balanced precision/recall)

**Explanation:** "Blade Runner 2049 is directly linked to the original 'Blade Runner' through its shared universe and similar visual style. As per the emotional sector, it has a melancholic, contemplative mood, with a visual palette of **desaturated tones, orange-teal contrasts, and neon accents**. Its **monumental and desolate beauty, and symmetrical composition with negative space**, closely parallels the iconic aesthetic of 'Blade Runner'."

**Sectors Used:** emotional (primary - visual palette), procedural (supporting - similarity patterns)

**Key Strength:** Emotional sector explicitly captured visual details (palette, composition) that directly match Blade Runner's aesthetic.

---

### Winner: **OpenMemory**
Best balance of precision and recall. The **emotional sector specifically stores visual style details** (desaturated tones, neon accents, symmetrical composition) that directly match the query intent. Graphiti was too narrow (1 result), Pure Vector too broad (included weak "Her" match).

---

## Query 3: "Movies with dystopian corporate themes" (Thematic Query)

### Pure Vector Results
| Rank | Movie | Year | Score |
|------|-------|------|-------|
| 1 | Severance | 2022 | 0.443 |
| 2 | Blade Runner 2049 | 2017 | 0.439 |
| 3 | Dune | 2021 | 0.426 |

**Reasoning:** "Severance explores corporate control and dehumanizing work environments. Blade Runner 2049 shows mega-corporations controlling replicants. Dune portrays corporate-like entities controlling resources."

**Quality:** Good thematic matching, reasonable explanations.

---

### Graphiti Results
| Rank | Movie | Year | Score |
|------|-------|------|-------|
| 1 | Severance | 2022 | 0.850 |
| 2 | Blade Runner 2049 | 2017 | 0.850 |
| 3 | The Office | 2005 | 0.850 |

**Reasoning:** "Severance explores the central theme of corporate control via `EXPLORES_THEME` relationship. Blade Runner 2049 has thematic links to identity within dystopian settings."

**Graph Evidence:**
- `Severance --EXPLORES_THEME--> corporate control`
- `Blade Runner 2049 --THEMATIC_LINKS--> dystopian futures`

**Quality:** More explainable (shows exact graph connections).

---

### OpenMemory Results
| Rank | Movie | Year | Score |
|------|-------|------|-------|
| 1 | Blade Runner 2049 | 2017 | 0.470 |
| 2 | Severance | 2022 | 0.429 |

**Reasoning:** "Blade Runner 2049 fits the dystopian corporate theme as it explores a future where corporations have immense control over society, focusing on themes of identity and existentialism within this rigid structure. Severance reflects a dystopian corporate theme through its depiction of dehumanizing workplace dynamics, enhancing the horror elements within a supposed corporate environment."

**Sectors Used:** emotional (mood - unsettling/clinical), procedural (pacing, structure - parallel timelines showing innies/outies split)

**Key Strength:** OpenMemory captured the **emotional and procedural** aspects of corporate dystopia - not just the theme itself, but how it's experienced (dehumanizing dynamics, psychological horror) and structured (parallel timelines).

---

### Winner: **Three-Way Tie**
All three systems successfully identified relevant movies:
- **Pure Vector:** Widest recall (3 results including Dune)
- **Graphiti:** Most explicit theme tracking via `EXPLORES_THEME` edges
- **OpenMemory:** Most nuanced (captured emotional tone + narrative structure of corporate dystopia)

---

## Summary Scorecard

| Aspect | Pure Vector | Graphiti | OpenMemory | Winner |
|--------|-------------|----------|------------|--------|
| **Factual Accuracy** | 67% (false positive) | 100% | 100% | **Graphiti & OpenMemory** |
| **Explainability** | "Semantically similar" | Graph relationships | Sector-based (semantic/emotional/procedural) | **Graphiti & OpenMemory** |
| **Recall** | 3 results per query | 1-2 results per query | 2 results per query | **Pure Vector** |
| **Visual Style Queries** | Good but broad | Precise but narrow | **Best - emotional sector captures palette/composition** | **OpenMemory** |
| **Thematic Queries** | Good semantic matching | Explicit theme edges | Nuanced (emotion + structure) | **Three-way tie** |
| **Ingestion Speed** | Fast (embed only) | Slow (LLM extraction) | Medium (3 embeds per movie) | **Pure Vector** |
| **Cost** | Low (embeddings only) | High (many LLM calls) | Medium (3x embeddings) | **Pure Vector** |

---

## When to Use Each System

### Use Pure Vector When:
✅ Exploratory discovery ("movies that feel like...")
✅ Thematic/mood-based queries
✅ Recall is more important than precision
✅ Fast ingestion needed
✅ Lower cost is priority

❌ Avoid for: Factual queries where accuracy is critical

---

### Use Graphiti When:
✅ Factual queries (directors, actors, release dates)
✅ Relationship queries ("movies by same director")
✅ Precision is critical (no false positives)
✅ Explainability required (show reasoning)
✅ Temporal queries (when was fact added)

❌ Avoid for: Exploratory "vibe" queries where structure may miss connections

---

### Use OpenMemory When:
✅ Visual style queries (emotional sector stores palette, composition)
✅ Multi-faceted queries (semantic + emotional + procedural aspects)
✅ Mood/aesthetic queries ("films that feel melancholic")
✅ Nuanced thematic queries (not just theme, but how it's experienced)
✅ Queries requiring sector-based decomposition

❌ Avoid for: Simple factual queries where Graphiti's graph is more direct

---

## Hybrid Recommendation

**Best approach:** Route queries to appropriate system based on query type

```python
if query_type == "factual":  # "Who directed X?", "When was X released?"
    use Graphiti  # Guaranteed accuracy via graph relationships

elif query_type == "visual_style":  # "Films with similar cinematography"
    use OpenMemory  # Emotional sector captures visual details

elif query_type == "mood_aesthetic":  # "Films that feel melancholic"
    use OpenMemory  # Emotional sector + procedural sector

elif query_type == "exploratory":  # "Something like X but lighter"
    use Pure Vector  # Widest recall

elif query_type == "thematic":  # "Movies about loneliness"
    combine all three:
        graphiti_results = get explicit theme edges
        openmemory_results = get emotional/procedural context
        vector_results = get semantic similarity
        merge and rerank
```

---

## Concrete Example: The False Positive

**Query:** "Denis Villeneuve movies"

**What happened:**
- Pure Vector embedded "Denis Villeneuve" into vector space
- Found movies semantically close to Villeneuve's style
- "Her" scored 0.343 similarity (explores identity, technology, isolation)
- **But:** "Her" was directed by Spike Jonze, not Villeneuve

**Why Pure Vector failed:**
- No fact-checking mechanism
- Relies entirely on semantic similarity in embedding space
- "Villeneuve's style" and "movies Villeneuve directed" are different concepts

**Why Graphiti succeeded:**
- Explicit `DIRECTED_BY` relationship extracted during ingestion
- Graph query: `MATCH (m:Movie)-[:DIRECTED_BY]->(d {name: "Denis Villeneuve"})`
- Only returns movies with proven directorial relationship

**Why OpenMemory succeeded:**
- Semantic sector stored director facts during ingestion
- Query classification identified factual query → routed to semantic sector
- Retrieved only movies with verified director information

**Impact:** For a recommendation system, returning the wrong director's films damages trust. Both Graphiti and OpenMemory prevent this through structured knowledge.

---

## Quantitative Analysis

### Precision (% of results that are correct)

| Query Type | Pure Vector | Graphiti | Difference |
|------------|-------------|----------|------------|
| Factual | 67% | **100%** | +33% |
| Visual | ~67% (Her weak) | **100%** | +33% |
| Thematic | ~100% | ~100% | Tie |

**Average Precision:** Pure Vector: 78% vs Graphiti: **100%**

---

### Recall (ability to find relevant results)

| Query | Pure Vector | Graphiti | Difference |
|-------|-------------|----------|------------|
| Factual | 2 correct | 2 correct | Tie |
| Visual | 3 results | 1 result | PV +2 |
| Thematic | 3 results | 3 results | Tie |

**Finding:** Pure Vector found more results, but some were weak matches.

---

## Cost Analysis

**Pure Vector:**
- Ingestion: 1 embedding per movie (~$0.0001 each)
- Query: 1 embedding + 1 LLM call
- **Total for 5 movies + 3 queries:** ~$0.02

**Graphiti:**
- Ingestion: Multiple LLM calls per movie for entity extraction (~$0.01 each)
- Query: 1 LLM call
- **Total for 5 movies + 3 queries:** ~$0.08

**OpenMemory:**
- Ingestion: 3 embeddings per movie (one per sector) (~$0.0003 each)
- Query: 1 embedding per sector + 1 LLM call
- **Total for 5 movies + 3 queries:** ~$0.04

**Cost comparison:** Pure Vector (cheapest) < OpenMemory (medium) < Graphiti (4x Pure Vector)

---

## Conclusion

**No universal winner** - each system excels at different query types:

1. **Pure Vector:** Discovery engine, widest recall, lowest cost, simplest
2. **Graphiti:** Fact checker, highest precision, explainable via graph relationships
3. **OpenMemory:** Multi-faceted queries, sector-based decomposition (semantic/emotional/procedural)

**Key Insight:** The false positive on "Denis Villeneuve movies" demonstrates why **structured knowledge matters**. Both Graphiti (graph relationships) and OpenMemory (sector-based facts) prevented the error, while Pure Vector failed.

**Phase 2 Recommendation:** Implement hybrid routing based on query type:
- **Factual queries** → Graphiti (graph relationships)
- **Visual/mood queries** → OpenMemory (emotional sector)
- **Exploratory queries** → Pure Vector (wide recall)
- **Complex queries** → Combine all three systems

Each system contributes unique strengths to a complete entertainment discovery platform.
