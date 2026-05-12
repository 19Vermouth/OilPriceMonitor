from fastapi import APIRouter

from geip.schemas import EnergyConsumption

router = APIRouter()

DATA = [
    EnergyConsumption(region="Asia Pacific", country="China", consumption_twh=7500, year=2024),
    EnergyConsumption(region="Asia Pacific", country="India", consumption_twh=1800, year=2024),
    EnergyConsumption(region="North America", country="USA", consumption_twh=4000, year=2024),
    EnergyConsumption(region="Europe", country="Germany", consumption_twh=900, year=2024),
    EnergyConsumption(region="Middle East", country="Saudi Arabia", consumption_twh=450, year=2024),
]


@router.get("/consumption")
async def consumption():
    return {"data": DATA}
