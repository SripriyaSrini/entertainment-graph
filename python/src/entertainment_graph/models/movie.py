"""Movie schema matching Phase 1 spec."""

from typing import Literal
from pydantic import BaseModel


class Theme(BaseModel):
    name: str
    specificity: str | None = None
    prominence: Literal["central", "secondary", "subtle"]


class Mood(BaseModel):
    primary: list[str]
    undertones: list[str] = []
    intensity: Literal["subtle", "moderate", "intense"]
    emotional_arc: str | None = None


class VisualStyle(BaseModel):
    palette: list[str] = []
    composition: list[str] = []
    influences: list[str] = []
    descriptors: list[str] = []


class NarrativeStyle(BaseModel):
    pacing: str
    structure: str
    tone: str
    perspective: str | None = None


RelationType = Literal[
    "visual_style",
    "thematic",
    "mood",
    "narrative_style",
    "creator",
    "spiritual_successor",
    "contrast",
    "audience_overlap",
]


class SimilarityLink(BaseModel):
    target_id: str
    relationship_type: RelationType
    explanation: str
    strength: Literal[1, 2, 3, 4, 5]
    bidirectional: bool = True


class Movie(BaseModel):
    """Movie with semantic data for Phase 1 comparison."""

    # Identifiers
    id: str
    tmdb_id: int | None = None
    imdb_id: str | None = None

    # Basic metadata
    title: str
    year: int
    runtime_minutes: int | None = None
    genres: list[str] = []
    director: list[str] = []
    cast: list[str] = []
    plot_summary: str | None = None

    # Semantic data
    themes: list[Theme] = []
    mood: Mood | None = None
    visual_style: VisualStyle | None = None
    narrative: NarrativeStyle | None = None

    # Ground truth relationships
    similar_to: list[SimilarityLink] = []

    def to_text(self) -> str:
        """Flatten movie to text for embedding."""
        parts = [f"{self.title} ({self.year})"]

        if self.director:
            parts.append(f"Directed by {', '.join(self.director)}.")

        if self.genres:
            parts.append(f"Genres: {', '.join(self.genres)}.")

        if self.themes:
            theme_strs = [t.name for t in self.themes]
            parts.append(f"Themes: {', '.join(theme_strs)}.")

        if self.mood:
            parts.append(f"Mood: {', '.join(self.mood.primary)}.")

        if self.visual_style and self.visual_style.descriptors:
            parts.append(f"Visual style: {', '.join(self.visual_style.descriptors)}.")

        if self.narrative:
            parts.append(f"Pacing: {self.narrative.pacing}. Tone: {self.narrative.tone}.")

        if self.plot_summary:
            parts.append(self.plot_summary)

        return " ".join(parts)
