from datetime import datetime, timedelta, timezone
from random import uniform, gauss
from typing import Any

from geip.schemas import CrudeType


def calculate_volatility(prices: list[dict]) -> float:
    if len(prices) < 2:
        return 0.0
    values = [p.get("price", 0) for p in prices]
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return round(variance ** 0.5, 2)


def calculate_moving_average(prices: list[dict], window: int = 7) -> float:
    if len(prices) < window:
        return 0.0
    recent = [p.get("price", 0) for p in prices[-window:]]
    return round(sum(recent) / window, 2)


def calculate_change(prices: list[dict]) -> dict[str, float]:
    if len(prices) < 2:
        return {"daily": 0.0, "weekly": 0.0}
    
    current = prices[-1].get("price", 0)
    daily_prev = prices[-2].get("price", 0) if len(prices) >= 2 else current
    weekly_prev = prices[-7].get("price", 0) if len(prices) >= 7 else daily_prev
    
    daily_change = ((current - daily_prev) / daily_prev * 100) if daily_prev else 0
    weekly_change = ((current - weekly_prev) / weekly_prev * 100) if weekly_prev else 0
    
    return {
        "daily": round(daily_change, 2),
        "weekly": round(weekly_change, 2),
    }


def detect_anomalies(prices: list[dict], threshold: float = 2.0) -> list[dict[str, Any]]:
    if len(prices) < 3:
        return []
    
    values = [p.get("price", 0) for p in prices]
    mean = sum(values) / len(values)
    std = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
    
    anomalies = []
    for p in prices[-24:]:
        z_score = abs((p.get("price", 0) - mean) / std) if std > 0 else 0
        if z_score > threshold:
            anomalies.append({
                "timestamp": p.get("timestamp"),
                "price": p.get("price"),
                "z_score": round(z_score, 2),
                "type": "spike" if p.get("price", 0) > mean else "drop",
            })
    
    return anomalies


def generate_price_analytics() -> dict[str, Any]:
    base_prices = {
        "WTI": 78.50,
        "BRENT": 82.30,
        "DUBAI": 80.15,
        "OPEC_BASKET": 79.00,
    }
    
    history = []
    for crude, base in base_prices.items():
        prices = []
        for i in range(30):
            ts = datetime.now(timezone.utc) - timedelta(days=30-i)
            price = base + gauss(0, 1.5)
            prices.append({
                "crude_type": crude,
                "price": round(price, 2),
                "timestamp": ts.isoformat(),
            })
        history.append(prices)
    
    analytics = {}
    for crude, base in base_prices.items():
        prices = [p for h in history for p in h if p["crude_type"] == crude]
        change = calculate_change(prices)
        
        analytics[crude] = {
            "current": base,
            "ma_7": round(base + uniform(-1, 1), 2),
            "ma_30": round(base + uniform(-2, 2), 2),
            "volatility": round(uniform(0.5, 2.5), 2),
            "change_daily": round(change["daily"], 2),
            "change_weekly": round(change["weekly"], 2),
            "high_30d": round(base + uniform(2, 5), 2),
            "low_30d": round(base - uniform(2, 5), 2),
            "anomalies": detect_anomalies(prices),
        }
    
    return analytics


def generate_sentiment_analysis() -> dict[str, Any]:
    bullish = int(uniform(30, 50))
    bearish = int(uniform(20, 40))
    neutral = 100 - bullish - bearish
    
    return {
        "bullish_pct": bullish,
        "bearish_pct": bearish,
        "neutral_pct": neutral,
        "trend": "improving" if bullish > bearish else "declining",
        "articles_analyzed": 100,
    }


def generate_risk_trend() -> list[dict[str, Any]]:
    trends = []
    for i in range(30):
        ts = datetime.now(timezone.utc) - timedelta(days=30-i)
        score = 60 + uniform(-10, 15)
        trends.append({
            "date": ts.strftime("%Y-%m-%d"),
            "score": round(score, 1),
            "level": "High" if score >= 70 else "Moderate" if score >= 50 else "Low",
        })
    return trends


def generate_energy_forecast() -> list[dict[str, Any]]:
    regions = ["Asia Pacific", "North America", "Europe", "Middle East", "Africa", "Latin America"]
    forecast = []
    for region in regions:
        forecast.append({
            "region": region,
            "current": int(uniform(500, 8000)),
            "forecast_1y": int(uniform(550, 8500)),
            "growth_pct": round(uniform(-2, 8), 1),
        })
    return forecast
