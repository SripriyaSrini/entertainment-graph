"""Health check endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from entertainment_graph.routers.query import get_systems

router = APIRouter(tags=["health"])


class SystemHealth(BaseModel):
    name: str
    healthy: bool


class HealthResponse(BaseModel):
    status: str
    systems: list[SystemHealth]
    version: str = "0.1.0"


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Check health of all systems."""
    systems = get_systems()
    system_health = []

    for name, system in systems.items():
        try:
            healthy = await system.health_check()
        except Exception:
            healthy = False
        system_health.append(SystemHealth(name=name, healthy=healthy))

    all_healthy = all(s.healthy for s in system_health) if system_health else True
    status = "healthy" if all_healthy else "degraded"

    return HealthResponse(status=status, systems=system_health)
