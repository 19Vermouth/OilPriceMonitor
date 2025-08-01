# Oil Price Monitoring & Analysis System

## 🌟 Problem Statement

The global oil market is highly volatile, with prices fluctuating due to geopolitical events, supply-demand changes, and economic factors. Financial analysts, energy traders, and policymakers need:

1. **Real-time price tracking** with anomaly detection
2. **Contextual explanations** for sudden price movements
3. **Historical trend analysis** with AI-powered insights
4. **Reliable data pipelines** that work despite API limitations

This system solves these challenges through an automated monitoring platform that combines live data feeds with AI analysis.

## 🚀 Key Accomplishments

- **Real-time Dashboard**: Visualizes WTI/Brent crude prices with 5-minute refresh intervals
- **Anomaly Detection**: Identifies statistically significant price movements (Z-score based)
- **News Correlation**: Links price changes to relevant market news events
- **AI Explanations**: Generates natural language summaries of market conditions using Mistral-7B
- **Resilient Architecture**: Multiple fallback mechanisms ensure continuous operation

## 🔄 System Process Flow

1. **Data Collection**:
   - Live price feeds from Alpha Vantage/yFinance APIs
   - News aggregation from NewsAPI/GNews
   
2. **Processing Pipeline**:
   ```mermaid
   graph TD
     A[Price Data] --> B{Anomaly?}
     B -->|Yes| C[Fetch Relevant News]
     B -->|No| D[Store Normal Data]
     C --> E[AI Analysis]
     E --> F[Generate Insights]
     F --> G[Store Annotated Data]
   ```

3. **User Interaction**:
   - Streamlit dashboard for visualization
   - Natural language Q&A about price movements
   - Alert system for significant events

## 🏗️ System Architecture

```
oil-price-monitor/
├── src/
│   ├── price_tracker.py       # Multi-source price data
│   ├── anomaly_detector.py    # Statistical analysis
│   ├── news_aggregator.py     # News collection & filtering
│   ├── ollama_analyzer.py     # Mistral-7B integration
│   ├── etl_pipeline.py        # Data storage
│   └── monitor.py            # Main orchestrator
├── data/                     # SQLite database
├── dashboard.py              # Streamlit UI
├── tests/                    # Unit tests
├── .env                      # Configuration
└── requirements.txt          # Dependencies
```

## 🛠️ Step-by-Step Setup

### 1. Prerequisites
```bash
# Clone repository
git clone https://github.com/yourrepo/oil-price-monitor.git
cd oil-price-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

### 2. Configuration
Create `.env` file:
```ini
# Required APIs
ALPHAVANTAGE_API_KEY="yourkey"
NEWSAPI_API_KEY="yourkey"
FINNHUB_API_KEY="yourkey"  # Recommended alternative

# Optional
ANOMALY_THRESHOLD=3.0      # Z-score for alerts
POLLING_INTERVAL=5         # Minutes between checks
```

### 3. Installation
```bash
pip install -r requirements.txt
ollama pull mistral  # Download AI model (~4GB)
```

### 4. Running the System
```bash
# Terminal 1: Start Ollama AI service
ollama serve

# Terminal 2: Run monitoring backend
python src/monitor.py

# Terminal 3: Launch dashboard
streamlit run dashboard.py
```

### 5. Access Dashboard
Open `http://localhost:8501` in your browser to see:
- Real-time price charts
- Anomaly alerts
- AI-generated market analysis
- Interactive Q&A

## 💻 Tech Stack

| Component          | Technology                          | Purpose                           |
|--------------------|-------------------------------------|-----------------------------------|
| **Data Collection**| Alpha Vantage, yFinance, NewsAPI    | Live price/news feeds             |
| **Anomaly Detection** | Statsmodels, Z-score analysis    | Identify significant movements    |
| **AI Analysis**    | Ollama + Mistral-7B                | News summarization & Q&A          |
| **Data Storage**   | SQLite                             | Time-series data persistence      |
| **Visualization**  | Streamlit + Plotly                 | Interactive dashboard             |
| **Orchestration**  | Python 3.10+                       | System coordination               |

## 🎯 Key Features

1. **Multi-Source Resilience**:
   - Automatic fallback between 3+ price APIs
   - News aggregation from financial sources only
   - Local caching during API outages

2. **Intelligent Analysis**:
   ```python
   # Sample AI prompt
   Analyze these oil market news events:
   {news_articles}
   
   Identify the 3 most significant factors affecting 
   current prices in bullet points.
   ```

3. **Professional-Grade Metrics**:
   - Anomaly confidence scores
   - Source attribution for all data points
   - Response time <2s for user queries

## 📈 Example Output

**Dashboard View**:
```
🛢️ WTI Crude: $75.42 ▲0.5% (1σ)
--------------------------------------------------
🔴 Anomaly Detected: 2023-11-15 14:30 (Z=3.2)

Key Drivers:
- OPEC+ announces production cuts
- Hurricane disrupts Gulf Coast refining
- EIA reports inventory draw of 2.1M barrels

Historical Correlation: 
92% match with 2019 supply disruption pattern

```
Line Chart 
<img width="1893" height="905" alt="image" src="https://github.com/user-attachments/assets/7f194014-5403-4d6e-8b13-7cb832cdedde" />
Pie Chart and Bar chart
<img width="1890" height="871" alt="image" src="https://github.com/user-attachments/assets/0cc33878-2f88-469a-8af4-addcdc73dcb5" />

**Market News Analysis**
<img width="1782" height="614" alt="image" src="https://github.com/user-attachments/assets/a7981ed1-286b-4ec8-a4d1-652169bf7619" />







