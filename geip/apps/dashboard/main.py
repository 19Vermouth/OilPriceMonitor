import streamlit as st
import requests
import plotly.express as px
from datetime import datetime

API_URL = "http://localhost:8000"

st.set_page_config(page_title="GEIP Dashboard", page_icon="🛢️", layout="wide")

st.title("Global Energy Intelligence Platform")
st.markdown("**Real-time energy market monitoring**")


@st.cache_data(ttl=300)
def get_prices():
    try:
        r = requests.get(f"{API_URL}/api/v1/prices/latest", timeout=5)
        return r.json().get("prices", [])
    except:
        return []


@st.cache_data(ttl=60)
def get_news(limit=5):
    try:
        r = requests.get(f"{API_URL}/api/v1/news/news", params={"limit": limit}, timeout=5)
        return r.json().get("articles", [])
    except:
        return []


def get_risk():
    try:
        r = requests.get(f"{API_URL}/api/v1/risk/global", timeout=5)
        return r.json()
    except:
        return {}


def get_alerts():
    try:
        r = requests.get(f"{API_URL}/api/v1/alerts/active", timeout=5)
        return r.json().get("alerts", [])
    except:
        return []


col1, col2, col3 = st.columns(3)

with col1:
    risk = get_risk()
    st.metric("Global Risk Score", f"{risk.get('global_score', 'N/A')}", risk.get("level", ""))

with col2:
    prices = get_prices()
    if prices:
        wti = next((p for p in prices if p["crude_type"] == "WTI"), {})
        st.metric("WTI Crude", f"${wti.get('price', 'N/A')}", "/barrel")

with col3:
    alerts = get_alerts()
    st.metric("Active Alerts", len(alerts))

st.divider()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Price Overview")
    
    if prices:
        df_prices = [{"Benchmark": p["crude_type"], "Price": p["price"]} for p in prices]
        fig = px.bar(df_prices, x="Benchmark", y="Price", color="Benchmark", title="Crude Oil Prices (USD/barrel)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Connect to API to see prices")

with col_right:
    st.subheader("Latest Energy News")
    articles = get_news(5)
    if articles:
        for article in articles[:5]:
            sentiment_emoji = "📈" if article.get("sentiment") == "bullish" else "📉" if article.get("sentiment") == "bearish" else "📰"
            st.write(f"{sentiment_emoji} **{article.get('title', 'No title')}**")
            st.caption(f"_{article.get('source', 'Unknown')} | {article.get('published_at', '')[:10]}_")
    else:
        st.info("No news available")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Energy Consumption by Region")
    consumption_data = [
        {"Region": "Asia Pacific", "TWh": 9300},
        {"Region": "North America", "TWh": 4000},
        {"Region": "Europe", "TWh": 3500},
        {"Region": "Middle East", "TWh": 1200},
    ]
    fig = px.pie(names=[c["Region"] for c in consumption_data], values=[c["TWh"] for c in consumption_data], title="Energy Consumption")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Risk by Region")
    risk_data = [
        {"Region": "Middle East", "Risk": 78},
        {"Region": "Africa", "Risk": 68},
        {"Region": "Asia Pacific", "Risk": 55},
        {"Region": "Latin America", "Risk": 52},
        {"Region": "Europe", "Risk": 42},
        {"Region": "North America", "Risk": 35},
    ]
    fig = px.bar(risk_data, x="Region", y="Risk", color="Risk", color_continuous_scale="RdYlGn_r", title="Geopolitical Risk Scores")
    st.plotly_chart(fig, use_container_width=True)
