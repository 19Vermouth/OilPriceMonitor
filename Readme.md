# GEIP - Global Energy Intelligence Platform

**Enterprise-grade real-time energy market data platform**

---

## Overview

GEIP is a production-grade data engineering platform for real-time monitoring and analysis of global energy markets. It provides:

- **Real-time oil price tracking** (WTI, Brent, Dubai, OPEC Basket)
- **Geopolitical risk monitoring** with regional risk scores
- **Ship tracking** for maritime logistics
- **Energy consumption analytics**
- **AI-powered market intelligence** (via Ollama/LLM)
- **Anomaly detection and alerting**

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Data Sources                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│  OilPriceAPI │ EIA │ GDELT │ NewsAPI │ AIS │ Weather APIs                   │
└─────────────────────────────────────┬───────────────────────────────────────┘
                                      │
                             ┌────────▼────────┐
                             │  Apache Kafka   │
                             │  (7 partitions) │
                             └────────┬────────┘
                                      │
┌─────────────────────────────────────┴───────────────────────────────────────┐
│                          Medallion Architecture                               │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────┐       ┌─────────┐       ┌─────────┐       ┌─────────────┐  │
│  │ BRONZE   │──────▶│ SILVER   │──────▶│ GOLD     │──────▶│ PostgreSQL  │  │
│  │ (Raw)    │       │(Cleaned) │       │(Business)│       │+ TimescaleDB│  │
│  │ Delta    │       │ Delta    │       │ Delta   │       │  Metadata   │  │
│  └─────────┘       └─────────┘       └─────────┘       └─────────────┘  │
│       │                                                        │             │
│       └───────────────────────────────────────────────────────┘             │
│                                     │                                          │
│  ┌─────────────────────────────────┴───────────────────────────────────────┐ │
│  │                          Serving Layer                                   │ │
│  ├─────────────────────────────────────────────────────────────────────────┤ │
│  │   FastAPI (REST)    │    Next.js + Tailwind (Dashboard)   │    Prefect   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Features

### Core Capabilities
| Feature | Description | Status |
|---------|-------------|--------|
| Multi-Benchmark Prices | WTI, Brent, Dubai, OPEC Basket | ✅ |
| Geopolitical Risk | Global & regional risk scores | ✅ |
| Ship Tracking | AIS-based vessel positions | ✅ |
| Energy Consumption | Regional demand analytics | ✅ |
| Alerting | Configurable price/risk alerts | ✅ |
| Anomaly Detection | Z-score based price spikes | 🔄 |

### Data Sources
| Source | Type | Status |
|--------|------|--------|
| OilPriceAPI | Prices | 🔄 |
| EIA | Production/Inventory | 🔄 |
| GDELT | Geopolitical Events | 🔄 |
| NewsAPI | News Articles | 🔄 |
| AIS | Ship Positions | 🔄 |

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Streaming** | Apache Kafka | Real-time data ingestion |
| **Storage** | MinIO + Delta Lake | S3-compatible data lake |
| **Database** | PostgreSQL + TimescaleDB | Metadata & time-series |
| **Cache** | Redis | Query acceleration |
| **API** | FastAPI | REST API endpoints |
| **Dashboard** | Streamlit | Operational UI |
| **Orchestration** | Prefect | Pipeline scheduling |
| **Observability** | Prometheus + Grafana | Monitoring |

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- 8GB RAM minimum

### 1. Clone and Setup

```bash
git clone https://github.com/yourorg/geip.git
cd geip
cp .env.example .env
# Edit .env and add your API keys
```

### 2. Start Infrastructure

```bash
docker compose -f infrastructure/docker/docker-compose.yml up -d
```

This starts:
- **Redis**: port 6379 (caching)
- **PostgreSQL**: port 5432 (metadata)
- **MinIO**: ports 9000/9001 (data lake)
- **Prometheus**: port 9090 (metrics)
- **Grafana**: port 3001 (dashboards)

### 3. Create Virtual Environment & Install

Using **uv** (recommended - 10-100x faster):

```bash
# Create venv with uv
uv venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\Activate

# Install dependencies
uv pip install -e .

# With dev tools (linting, testing)
uv pip install -e ".[dev]"
```

Using **pip** (alternative):

```bash
python -m venv .venv
source .venv/Scripts/activate

pip install -e ".[all]"
```

### 4. Run Services

**Backend (FastAPI):**
```bash
cd geip
uvicorn geip.apps.api.main:app --reload
```

**Frontend (Next.js):**
```bash
cd web
npm install
npm run dev
```

Access at: http://localhost:3000

### 5. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Dashboard (Next.js) | http://localhost:3000 | - |
| API Docs | http://localhost:8000/docs | - |
| Metrics | http://localhost:8000/metrics | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3001 | admin/admin |
| MinIO Console | http://localhost:9001 | minioadmin/minioadmin |

## Project Structure

```
geip/                          # Python backend
├── apps/
│   ├── api/                    # FastAPI REST API
│   │   ├── main.py           # Application entry
│   │   └── routers/         # API endpoints
│   └── dashboard/             # Legacy Streamlit (replaced by web/)
├── ingestion/                 # Data connectors
├── schemas/                   # Pydantic models
├── infrastructure/            # Docker configs
└── pyproject.toml

web/                           # Next.js frontend
├── app/                      # App router pages
│   ├── layout.tsx           # Root layout with nav
│   └── page.tsx             # Dashboard page
├── components/
│   ├── ui/                  # Reusable UI (Card, Badge)
│   └── dashboard/           # Dashboard widgets
├── lib/
│   ├── api.ts              # API client
│   └── utils.ts            # Utilities
└── types/                   # TypeScript types
```

## API Endpoints

### Health
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Basic health check |
| `/health/live` | GET | Liveness probe |
| `/health/ready` | GET | Readiness probe |

### Prices
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/prices/latest` | GET | Latest prices for all benchmarks |
| `/api/v1/prices/{crude_type}` | GET | Current price for specific benchmark |
| `/api/v1/prices/history` | GET | Historical price data |

### Risk
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/risk/global` | GET | Global risk score |
| `/api/v1/risk/region/{region}` | GET | Regional risk score |
| `/api/v1/risk/chokepoints` | GET | Maritime chokepoint risks |

### Ships
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/ships/live` | GET | Live vessel positions |
| `/api/v1/ships/congestion` | GET | Port/chokepoint congestion |
| `/api/v1/ships/{mmsi}` | GET | Vessel details |

### Energy
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/energy/consumption` | GET | Consumption data |
| `/api/v1/energy/production` | GET | Production data |
| `/api/v1/energy/inventory` | GET | Inventory levels |

### Alerts
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/alerts/active` | GET | Active alerts |
| `/api/v1/alerts` | POST | Create alert |
| `/api/v1/alerts/{id}` | GET | Get alert by ID |
| `/api/v1/alerts/{id}` | PATCH | Update alert |

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# API Keys (required)
OILPRICEAPI_KEY=your_key_here
NEWSAPI_API_KEY=your_key_here

# Infrastructure (defaults shown)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
POSTGRES_HOST=localhost
POSTGRES_DB=geip
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Development

### Code Quality

```bash
# Lint (with uv run - no install needed)
uv run ruff check .

# Format
uv run ruff format .

# Type check
uv run mypy geip/

# Run tests
uv run pytest tests/ -v

# Run all checks
uv run ruff check . && uv run mypy geip/
```

### Pre-commit Hooks

```bash
uv pip install pre-commit
pre-commit install
```

## Monitoring

### Prometheus Metrics

Custom metrics exposed at `/metrics`:
- `geip_prices_total` - Total price fetches
- `geip_api_requests_total` - API request count
- `geip_api_latency_seconds` - API latency histogram
- `geip_kafka_messages_produced` - Kafka message count

### Grafana Dashboards

Pre-configured dashboards:
- **GEIP Overview** - System health
- **API Performance** - Latency, errors
- **Pipeline Status** - Data freshness

## Deployment

### Docker Compose (Recommended for MVP)

```bash
docker compose -f infrastructure/docker/docker-compose.yml up -d
```

### Kubernetes

Manifests provided in `infrastructure/k8s/`:

```bash
kubectl apply -f infrastructure/k8s/
```

## Troubleshooting

### Kafka Not Starting
```bash
# Check Kafka logs
docker logs geip-kafka

# Wait longer (Kafka takes ~60s to start)
sleep 60
docker compose -f infrastructure/docker/docker-compose.yml restart kafka
```

### MinIO Bucket Not Found
```bash
# Run setup again
docker compose -f infrastructure/docker/docker-compose.yml up minio-setup -d
```

### API Returns 503
```bash
# Check dependencies are healthy
curl http://localhost:5432  # PostgreSQL
curl http://localhost:6379  # Redis
curl http://localhost:9092   # Kafka
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file

## Support

- **Issues**: GitHub Issues
- **Documentation**: [docs/](docs/)
- **Discussions**: GitHub Discussions
