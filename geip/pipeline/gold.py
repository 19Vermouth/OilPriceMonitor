import pandas as pd
from datetime import datetime, timezone, timedelta

from geip.storage import lake_manager


def aggregate_prices_daily():
    df = lake_manager.read_table("silver", "prices", limit=10000)
    if df.empty:
        return
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    
    daily = df.groupby(["crude_type", "date"]).agg(
        avg_price=("price", "mean"),
        min_price=("price", "min"),
        max_price=("price", "max"),
        count=("price", "count"),
    ).reset_index()
    
    daily["aggregation_date"] = datetime.now(timezone.utc).isoformat()
    lake_manager.write_silver("prices_daily", daily.to_dict("records"))


def aggregate_news_sentiment():
    df = lake_manager.read_table("silver", "news", limit=1000)
    if df.empty:
        return
    
    sentiment_counts = df["sentiment"].value_counts().to_dict()
    
    result = {
        "bullish_count": sentiment_counts.get("bullish", 0),
        "bearish_count": sentiment_counts.get("bearish", 0),
        "neutral_count": sentiment_counts.get("neutral", 0),
        "total_articles": len(df),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    
    lake_manager.write_silver("news_sentiment_summary", [result])


def aggregate_energy_by_region():
    df = lake_manager.read_table("silver", "energy", limit=1000)
    if df.empty:
        return
    
    by_region = df.groupby("region").agg(
        total_consumption=("consumption_twh", "sum"),
        avg_consumption=("consumption_twh", "mean"),
        country_count=("country", "nunique"),
    ).reset_index()
    
    by_region["aggregation_date"] = datetime.now(timezone.utc).isoformat()
    lake_manager.write_silver("energy_by_region", by_region.to_dict("records"))


def aggregate_risk_trends():
    df = lake_manager.read_table("silver", "risk", limit=1000)
    if df.empty:
        return
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    
    trends = df.groupby("date").agg(
        avg_risk_score=("global_score", "mean"),
        max_risk_score=("global_score", "max"),
        min_risk_score=("global_score", "min"),
        count=("global_score", "count"),
    ).reset_index()
    
    trends["aggregation_date"] = datetime.now(timezone.utc).isoformat()
    lake_manager.write_silver("risk_trends", trends.to_dict("records"))


def run_all():
    aggregate_prices_daily()
    aggregate_news_sentiment()
    aggregate_energy_by_region()
    aggregate_risk_trends()
