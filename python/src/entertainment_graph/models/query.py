"""Query and response models for agentic systems."""

from pydantic import BaseModel


class QueryResult(BaseModel):
    """A single result from an agentic query."""

    id: str
    title: str
    year: int
    score: float
    explanation: str  # LLM-generated explanation
    retrieval_context: dict = {}  # What the system provided to the LLM


class AgentResponse(BaseModel):
    """Response from an agentic system."""

    results: list[QueryResult]
    reasoning: str  # How the agent interpreted the query
    system_name: str  # Which system generated this
