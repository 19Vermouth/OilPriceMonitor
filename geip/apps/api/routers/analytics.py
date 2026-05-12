from fastapi import APIRouter

from geip.analytics import (
    generate_price_analytics,
    generate_sentiment_analysis,
    generate_risk_trend,
    generate_energy_forecast,
)

router = APIRouter()


@router.get("/prices")
async def price_analytics():
    return generate_price_analytics()


@router.get("/sentiment")
async def sentiment_analysis():
    return generate_sentiment_analysis()


@router.get("/risk/trend")
async def risk_trend():
    return {"trends": generate_risk_trend()}


@router.get("/energy/forecast")
async def energy_forecast():
    return {"forecast": generate_energy_forecast()}


@router.get("/summary")
async def analytics_summary():
    return {
        "prices": generate_price_analytics(),
        "sentiment": generate_sentiment_analysis(),
        "risk_trend": generate_risk_trend()[-7:],
        "energy_forecast": generate_energy_forecast(),
    }
