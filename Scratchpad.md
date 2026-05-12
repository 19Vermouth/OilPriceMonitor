# GEIP Scratchpad

## Development Notes

### Current Phase
- [x] Phase 1: Foundation (Complete)
- [x] Phase 2: Ingestion Layer (Complete - OilPriceAPI + NewsAPI connected)
- [x] Phase 2b: Medallion Pipeline (Complete - Bronze/Silver/Gold)
- [x] Phase 5: Observability (Complete - Prometheus metrics)
- [x] Phase 6: Dashboard & Visualizations (Complete - Next.js)
- [x] Phase 3: Storage & Query Layer (Complete - PostgreSQL + SQLAlchemy)
- [ ] Phase 7: Geospatial Features
- [ ] Phase 8: ML/AI Layer
- [ ] Phase 9: CI/CD & Documentation

### Ideas & TODOs

#### High Priority
- [x] Implement OilPriceAPI connector with retry logic
- [x] Implement NewsAPI connector with fallback
- [x] Set up Delta Lake tables
- [x] Add Prometheus metrics
- [x] Add Redis caching for API responses
- [x] Implement PostgreSQL metadata storage
- [ ] Implement anomaly detection

#### Medium Priority
- [ ] Create Prefect DAGs for orchestration
- [ ] Set up Grafana dashboards

#### Low Priority
- [ ] Implement ship tracking (AIS)
- [ ] Add geopolitical heat map
- [ ] Create ML forecasting models
- [ ] Set up Grafana dashboards

### Questions to Resolve
- [ ] Should we use dbt for transformations or PySpark?
- [ ] Kafka vs Redpanda for streaming?
- [ ] Docker Compose vs Kubernetes for deployment?

### API Endpoints Implemented
- [x] `/health` - Health check
- [x] `/api/v1/prices/latest` - Latest prices (OilPriceAPI)
- [x] `/api/v1/prices/history` - Price history
- [x] `/api/v1/risk/global` - Global risk score
- [x] `/api/v1/ships/live` - Ship positions
- [x] `/api/v1/energy/consumption` - Energy data
- [x] `/api/v1/alerts/active` - Active alerts
- [x] `/api/v1/news/news` - Energy news (NewsAPI)

### Bugs Found
- [ ] None yet (project is new)

### Performance Considerations
- Redis caching for sub-second response times
- Partition pruning for Delta Lake queries
- Connection pooling for PostgreSQL

### Security Notes
- API keys stored in environment variables
- No secrets in code
- CORS configured for specific origins

### Testing Strategy
- Unit tests for schemas and connectors
- Integration tests for API endpoints
- E2E tests for dashboard flows

---

## Quick Commands

```bash
# Start infrastructure
docker compose -f infrastructure/docker/docker-compose.yml up -d

# Install dependencies
pip install -e ".[all]"

# Run API
uvicorn geip.apps.api.main:app --reload

# Run Dashboard
streamlit run geip/apps/dashboard/main.py

# Run tests
pytest tests/ -v
```

---

## API Keys Needed

- [x] OilPriceAPI Key (user has)
- [ ] EIA API Key (not available)
- [x] NewsAPI Key (user has)
- [ ] GNews Key (optional)
- [ ] GDELT (free, no key)

---

## Reference Links

- OilPriceAPI: https://oilpriceapi.com/
- EIA Open Data: https://www.eia.gov/opendata/
- GDELT: https://gdeltproject.org/
- Kafka: https://kafka.apache.org/
- Delta Lake: https://delta.io/
