"""Base class for all agentic retrieval systems."""

from abc import ABC, abstractmethod

from entertainment_graph.models import Movie, AgentResponse


class AgenticSystem(ABC):
    """
    Common interface for all agentic retrieval systems.

    Each implementation includes LLM reasoning, not just raw retrieval.
    The flow for each system:
    1. System retrieves relevant context (memories, graph nodes, etc.)
    2. LLM reasons over the context
    3. Returns results with explanations
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """System name for display."""
        pass

    @abstractmethod
    async def ingest(self, movies: list[Movie]) -> int:
        """Ingest movies into the system. Returns count ingested."""
        pass

    @abstractmethod
    async def query(self, query: str, limit: int = 5) -> AgentResponse:
        """
        Full agentic query:
        1. System retrieves relevant context
        2. LLM reasons over the context
        3. Returns results with explanations
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if system is available."""
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all data from the system."""
        pass
