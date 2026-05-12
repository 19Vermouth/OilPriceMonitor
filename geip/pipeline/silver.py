import pandas as pd
from datetime import datetime, timezone

from geip.storage import lake_manager


def clean_prices():
    df = lake_manager.read_table("bronze", "prices", limit=1000)
    if df.empty:
        return
    
    df_clean = df.copy()
    df_clean["price"] = pd.to_numeric(df_clean["price"], errors="coerce")
    df_clean = df_clean.dropna(subset=["price"])
    df_clean = df_clean.drop_duplicates(subset=["crude_type", "timestamp"])
    
    lake_manager.write_silver("prices", df_clean.to_dict("records"))


def clean_news():
    df = lake_manager.read_table("bronze", "news", limit=1000)
    if df.empty:
        return
    
    df_clean = df.copy()
    df_clean = df_clean.dropna(subset=["title"])
    df_clean = df_clean.drop_duplicates(subset=["title"])
    df_clean["sentiment"] = df_clean["sentiment"].fillna("neutral")
    
    lake_manager.write_silver("news", df_clean.to_dict("records"))


def clean_risk():
    df = lake_manager.read_table("bronze", "risk", limit=1000)
    if df.empty:
        return
    
    df_clean = df.copy()
    df_clean["global_score"] = pd.to_numeric(df_clean["global_score"], errors="coerce")
    df_clean = df_clean.dropna(subset=["global_score"])
    
    lake_manager.write_silver("risk", df_clean.to_dict("records"))


def clean_energy():
    df = lake_manager.read_table("bronze", "energy", limit=1000)
    if df.empty:
        return
    
    df_clean = df.copy()
    df_clean["consumption_twh"] = pd.to_numeric(df_clean["consumption_twh"], errors="coerce")
    df_clean = df_clean.dropna(subset=["consumption_twh"])
    
    lake_manager.write_silver("energy", df_clean.to_dict("records"))


def run_all():
    clean_prices()
    clean_news()
    clean_risk()
    clean_energy()
