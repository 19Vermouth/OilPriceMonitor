import streamlit as st
import pandas as pd
import plotly.express as px
from src.news_aggregator import NewsAggregator
from src.ollama_analyzer import OilPriceChangeAnalyzer
import sqlite3

# Page Configuration
st.set_page_config(
    page_title="Oil Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {background-color: #f8f9fa;}
    .stAlert {padding: 20px;}
    .css-18e3th9 {padding: 2rem 5rem;}
</style>
""", unsafe_allow_html=True)

# Sample Data (in a real app, you'd query your database)
def get_price_data():
    return pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=90, freq='D'),
        'WTI Price': [72 + x*0.1 + 2*(x%7) for x in range(90)],
        'Brent Price': [75 + x*0.08 + 1.5*(x%5) for x in range(90)]
    })

def get_market_share():
    return pd.DataFrame({
        'Country': ['USA', 'Saudi Arabia', 'Russia', 'Canada', 'Iraq', 'Others'],
        'Share': [18.9, 15.5, 12.6, 9.8, 8.5, 34.7],
        'Profit (2024)': [120, 180, 90, 60, 45, 150]  # $Billion
    })

# Dashboard Layout
def main():
    st.title("🛢️ Global Oil Market Dashboard")
    
    # ---- Row 1: Price Charts ----
    st.header("Crude Oil Price Trends")
    price_data = get_price_data()
    
    fig1 = px.line(
        price_data,
        x='Date',
        y=['WTI Price', 'Brent Price'],
        labels={'value': 'Price ($/barrel)', 'variable': 'Benchmark'},
        color_discrete_map={
            'WTI Price': '#1f77b4',
            'Brent Price': '#ff7f0e'
        }
    )
    fig1.update_layout(
        hovermode="x unified",
        showlegend=True,
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # ---- Row 2: Market Share & Profit ----
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Global Production Share")
        share_data = get_market_share()
        
        fig2 = px.pie(
            share_data,
            names='Country',
            values='Share',
            hole=0.4,
            color='Country',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig2.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>%{percent} of global production"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("Annual Profits (2024)")
        fig3 = px.bar(
            share_data.sort_values('Profit (2024)', ascending=False),
            x='Country',
            y='Profit (2024)',
            color='Country',
            labels={'Profit (2024)': 'Profit ($ Billion)'},
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig3.update_layout(showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)
    
    # ---- Row 3: News Analysis ----
    st.header("Market News Analysis")
    if st.button("🔄 Get Latest Analysis"):
        with st.spinner("Analyzing market conditions..."):
            aggregator = NewsAggregator()
            analyzer = OilPriceChangeAnalyzer()
            
            articles = aggregator.fetch_price_change_reasons()
            if articles:
                analysis = analyzer.analyze_price_change(articles)
                
                st.subheader("Key Market Drivers")
                cols = st.columns(2)
                for i, reason in enumerate(analysis.get('reasons', [])):
                    cols[i%2].markdown(f"🔹 {reason}")
                
                with st.expander("📰 View Detailed News Analysis"):
                    st.write(analysis.get('raw_response', 'No detailed analysis available'))
            else:
                st.warning("Could not fetch current market news")

if __name__ == "__main__":
    main()