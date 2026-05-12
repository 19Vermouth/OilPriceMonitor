from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class CrudeType(str, Enum):
    WTI = "WTI"
    BRENT = "BRENT"
    DUBAI = "DUBAI"
    OPEC_BASKET = "OPEC_BASKET"


class Region(str, Enum):
    MIDDLE_EAST = "MIDDLE_EAST"
    NORTH_AMERICA = "NORTH_AMERICA"
    EUROPE = "EUROPE"
    ASIA_PACIFIC = "ASIA_PACIFIC"
    AFRICA = "AFRICA"
    LATIN_AMERICA = "LATIN_AMERICA"


class PriceData(BaseModel):
    crude_type: CrudeType
    price: float
    unit: str = "USD/barrel"
    timestamp: datetime


class RiskScore(BaseModel):
    region: Region | None = None
    global_score: float = Field(ge=0, le=100)
    level: str
    factors: list[str] = []


class ShipPosition(BaseModel):
    mmsi: str
    name: str
    latitude: float
    longitude: float
    heading: float | None = None
    speed: float | None = None
    timestamp: datetime


class EnergyConsumption(BaseModel):
    region: str
    country: str | None = None
    consumption_twh: float
    year: int


class Alert(BaseModel):
    id: str
    type: str
    message: str
    severity: str
    is_active: bool = True
    created_at: datetime


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "0.1.0"
