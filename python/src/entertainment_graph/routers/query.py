"""Query endpoints for comparing retrieval systems."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from entertainment_graph.systems import AgenticSystem
from entertainment_graph.models import AgentResponse

router = APIRouter(prefix="/query", tags=["query"])

# Systems registry - populated at startup
_systems: dict[str, AgenticSystem] = {}


def register_system(name: str, system: AgenticSystem) -> None:
    """Register a system for querying."""
    _systems[name] = system


def get_systems() -> dict[str, AgenticSystem]:
    """Get all registered systems."""
    return _systems


class QueryRequest(BaseModel):
    query: str
    limit: int = 5


class ComparisonResponse(BaseModel):
    query: str
    responses: dict[str, AgentResponse]


@router.post("/{system_name}", response_model=AgentResponse)
async def query_system(system_name: str, request: QueryRequest) -> AgentResponse:
    """Query a specific system."""
    if system_name not in _systems:
        raise HTTPException(
            status_code=404,
            detail=f"System '{system_name}' not found. Available: {list(_systems.keys())}",
        )

    system = _systems[system_name]
    return await system.query(request.query, request.limit)


@router.post("/compare", response_model=ComparisonResponse)
async def compare_all(request: QueryRequest) -> ComparisonResponse:
    """Query all systems and compare results."""
    responses = {}
    for name, system in _systems.items():
        try:
            responses[name] = await system.query(request.query, request.limit)
        except Exception as e:
            responses[name] = AgentResponse(
                results=[],
                reasoning=f"Error: {str(e)}",
                system_name=name,
            )

    return ComparisonResponse(query=request.query, responses=responses)


@router.get("/systems")
async def list_systems() -> list[str]:
    """List available systems."""
    return list(_systems.keys())
