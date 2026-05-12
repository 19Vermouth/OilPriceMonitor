from datetime import datetime, timezone

from fastapi import APIRouter

from geip.schemas import ShipPosition

router = APIRouter()

SHIPS = [
    ShipPosition(mmsi="123456789", name="MT Tanker Alpha", latitude=25.5, longitude=55.3, heading=90, speed=12.5, timestamp=datetime.now(timezone.utc)),
    ShipPosition(mmsi="987654321", name="MT Tanker Beta", latitude=26.2, longitude=56.8, heading=180, speed=10.2, timestamp=datetime.now(timezone.utc)),
    ShipPosition(mmsi="456789123", name="MT Tanker Gamma", latitude=27.1, longitude=52.5, heading=270, speed=11.8, timestamp=datetime.now(timezone.utc)),
]


@router.get("/live")
async def live_ships():
    return {"ships": SHIPS}
