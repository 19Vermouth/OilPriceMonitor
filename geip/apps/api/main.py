from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from geip.apps.api.routers import alerts, energy, geo, health, news, prices, ships
from geip.apps.api.routers.analytics import router as analytics_router
from geip.monitoring import setup_metrics, api_logger
from geip.schemas import HealthResponse
from geip.storage.database import init_db, init_alerts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    api_logger.info("GEIP API starting up...")
    try:
        init_db()
        init_alerts()
        api_logger.info("Database initialized successfully")
    except Exception as e:
        api_logger.error(f"Database init failed: {e}")
    yield
    api_logger.info("GEIP API shutting down...")


app = FastAPI(
    title="GEIP API",
    description="Global Energy Intelligence Platform API",
    version="0.1.0",
    lifespan=lifespan,
)

setup_metrics(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(prices.router, prefix="/api/v1/prices", tags=["Prices"])
app.include_router(geo.router, prefix="/api/v1/risk", tags=["Risk"])
app.include_router(ships.router, prefix="/api/v1/ships", tags=["Ships"])
app.include_router(energy.router, prefix="/api/v1/energy", tags=["Energy"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(news.router, prefix="/api/v1/news", tags=["News"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])


@app.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(status="operational", timestamp=datetime.now(timezone.utc))
