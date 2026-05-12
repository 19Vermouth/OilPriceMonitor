# GEIP Product Requirements Document (PRD)

## 1. Introduction

### 1.1 Purpose
This document defines the product requirements for the **Global Energy Intelligence Platform (GEIP)**, an enterprise-grade real-time data platform for monitoring and analyzing global energy markets.

### 1.2 Scope
GEIP provides real-time oil price tracking, geopolitical risk monitoring, ship tracking, energy consumption analytics, and AI-powered market intelligence.

### 1.3 Target Users
- Energy traders and analysts
- Financial institutions
- Energy market researchers
- Government agencies
- Oil & gas companies

---

## 2. Product Overview

### 2.1 Core Features

#### 2.1.1 Real-Time Price Tracking
| Feature | Description | Priority |
|---------|-------------|----------|
| Multi-Benchmark Prices | WTI, Brent, Dubai, OPEC Basket | P0 |
| Price Alerts | Configurable thresholds | P0 |
| Historical Analysis | OHLCV data with aggregation | P0 |
| Anomaly Detection | Z-score based price spikes | P1 |

#### 2.1.2 Geopolitical Risk Monitoring
| Feature | Description | Priority |
|---------|-------------|----------|
| Global Risk Score | Aggregated risk by region | P0 |
| Chokepoint Monitoring | Strait of Hormuz, Suez, Panama | P0 |
| Event Tracking | Conflicts, sanctions, supply outages | P1 |
| Heat Map Visualization | Interactive world map | P2 |

#### 2.1.3 Ship Tracking
| Feature | Description | Priority |
|---------|-------------|----------|
| Live Vessel Positions | AIS-based tracking | P1 |
| Route Analysis | ETA and congestion metrics | P1 |
| Chokepoint Density | Traffic at key routes | P1 |

#### 2.1.4 Energy Consumption
| Feature | Description | Priority |
|---------|-------------|----------|
| Regional Demand | Country-level consumption | P1 |
| Production Data | Supply-side metrics | P1 |
| Inventory Levels | Storage and stocks | P1 |

#### 2.1.5 AI/ML Features
| Feature | Description | Priority |
|---------|-------------|----------|
| Price Forecasting | Prophet-based predictions | P2 |
| Sentiment Analysis | News sentiment scoring | P2 |
| Market Summaries | LLM-generated insights | P2 |

### 2.2 Data Sources

| Source | Data Type | Fallback | Priority |
|--------|-----------|----------|----------|
| OilPriceAPI | Oil Prices | EIA, yFinance | P0 |
| EIA | Production/Inventory | GDELT | P1 |
| GDELT | Geopolitical Events | NewsAPI | P1 |
| NewsAPI | News Articles | GNews | P1 |
| AIS Providers | Ship Positions | Sample Data | P2 |

---

## 3. User Requirements

### 3.1 Functional Requirements

#### FR-001: Price Data Ingestion
> The system shall ingest oil prices from OilPriceAPI at 5-minute intervals.

#### FR-002: Price Alerting
> The system shall generate alerts when prices exceed user-defined thresholds.

#### FR-003: Risk Score Calculation
> The system shall calculate geopolitical risk scores based on recent events.

#### FR-004: Historical Data Access
> The system shall provide API access to at least 1 year of historical price data.

#### FR-005: Dashboard Visualization
> The system shall display real-time prices on a web dashboard.

#### FR-006: Alert Management
> Users shall be able to create, view, acknowledge, and resolve alerts.

### 3.2 Non-Functional Requirements

#### NFR-001: Performance
- Dashboard page load: < 2 seconds
- API response time: < 500ms for cached queries
- Real-time update latency: < 30 seconds

#### NFR-002: Availability
- System uptime: 99.5%
- Planned maintenance window: Sunday 2-4 AM UTC

#### NFR-003: Scalability
- Support 100 concurrent dashboard users
- Process 10,000 price updates per day
- Store 5 years of historical data

#### NFR-004: Security
- All API endpoints require authentication
- API keys stored encrypted
- No sensitive data in logs

---

## 4. Technical Requirements

### 4.1 Data Architecture

#### Medallion Layers
```
BRONZE (Raw) → SILVER (Cleaned) → GOLD (Business)
```

| Layer | Retention | Purpose |
|-------|-----------|---------|
| Bronze | Indefinite | Immutable raw data |
| Silver | 2 years | Cleaned, deduplicated |
| Gold | 1 year | Aggregated metrics |

### 4.2 API Requirements

| Endpoint | Method | Auth | Rate Limit |
|----------|--------|------|------------|
| `/health` | GET | No | 100/min |
| `/api/v1/prices/*` | GET | Yes | 60/min |
| `/api/v1/risk/*` | GET | Yes | 60/min |
| `/api/v1/alerts` | GET/POST | Yes | 30/min |

### 4.3 Storage Requirements

| Store | Technology | Data Type | Size Estimate |
|-------|-----------|-----------|---------------|
| Raw Data | Delta Lake | Parquet | 100GB/year |
| Metadata | PostgreSQL | Relational | 10GB |
| Cache | Redis | Hot data | 1GB |
| ML Models | S3 | Serialized | 5GB |

---

## 5. User Stories

### US-001: Price Monitoring
**As a** trader, **I want to** see real-time oil prices, **so that I** can make informed trading decisions.

### US-002: Alert Configuration
**As a** analyst, **I want to** set price alerts, **so that I** am notified of significant movements.

### US-003: Risk Assessment
**As a** researcher, **I want to** view geopolitical risk scores, **so that I** can assess market stability.

### US-004: Historical Analysis
**As a** strategist, **I want to** query historical data, **so that I** can identify trends.

### US-005: Ship Tracking
**As a** logistics manager, **I want to** track vessel positions, **so that I** can estimate delivery times.

---

## 6. Acceptance Criteria

### AC-001: Price Ingestion
- [ ] Prices ingested from OilPriceAPI every 5 minutes
- [ ] Data stored in Bronze layer
- [ ] Fallback to EIA if OilPriceAPI fails

### AC-002: Dashboard
- [ ] All crude benchmarks displayed
- [ ] Price chart renders in < 2 seconds
- [ ] Responsive on mobile devices

### AC-003: Alerting
- [ ] Users can create price alerts
- [ ] Alerts trigger within 1 minute of threshold breach
- [ ] Alert history maintained for 90 days

### AC-004: API
- [ ] All endpoints documented in OpenAPI
- [ ] Response times < 500ms (cached)
- [ ] Authentication via API keys

### AC-005: Reliability
- [ ] System handles API source failures gracefully
- [ ] No data loss during infrastructure restarts
- [ ] Circuit breakers prevent cascade failures

---

## 7. Out of Scope

The following features are explicitly excluded from this release:

- Mobile application
- Multi-tenancy
- Real-time collaboration
- Custom indicator calculations
- Third-party integrations (Bloomberg, Reuters)
- Physical trading execution

---

## 8. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Dashboard Uptime | 99.5% | Prometheus monitoring |
| API Latency (p95) | < 500ms | APM tracking |
| Data Freshness | < 5 min | Timestamp comparison |
| Alert Accuracy | > 90% | Manual review |
| User Satisfaction | > 4/5 | User surveys |

---

## 9. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-01-01 | GEIP Team | Initial release |
