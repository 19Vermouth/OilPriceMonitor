from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from geip.ingestion import cache

router = APIRouter()


class HealthCheck(BaseModel):
    status: str
    redis: str
    timestamp: datetime


class ReadinessCheck(BaseModel):
    status: str
    checks: dict


@router.get("/", response_model=HealthCheck)
async def health():
    redis_status = "healthy" if cache.client else "unavailable"
    return HealthCheck(
        status="healthy",
        redis=redis_status,
        timestamp=datetime.now(timezone.utc)
    )


@router.get("/live")
async def liveness():
    return {"status": "alive"}


@router.get("/ready")
async def readiness():
    checks = {
        "redis": "ok" if cache.client else "degraded",
        "api": "ok",
    }
    all_ok = all(v == "ok" for v in checks.values())
    return ReadinessCheck(
        status="ready" if all_ok else "not_ready",
        checks=checks
    )
