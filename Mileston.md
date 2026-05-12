# GEIP Milestones

## Project Timeline

```
Start Date: TBD
Target Duration: 8-12 weeks (solo developer)
Work Schedule: Part-time (10-15 hours/week)
```

---

## Milestone Overview

| Milestone | Target Week | Status |
|-----------|-------------|--------|
| M0: Foundation | Week 1-2 | ✅ Complete |
| M1: Ingestion Layer | Week 3-4 | 🔄 In Progress |
| M2: Medallion Pipeline | Week 5-6 | ⏳ Pending |
| M3: Storage & API | Week 7-8 | ⏳ Pending |
| M4: Dashboard | Week 9-10 | ⏳ Pending |
| M5: Observability | Week 11-12 | ⏳ Pending |
| M6: Testing & Launch | Week 13-14 | ⏳ Pending |

---

## M0: Foundation (COMPLETE)

**Duration**: 2 weeks
**Goal**: Set up project structure and core infrastructure

### Deliverables
- [] Project directory structure
- [] `pyproject.toml` with dependencies
- [] Docker Compose with Kafka, MinIO, PostgreSQL, Redis
- [] Pydantic schemas for all domain models
- [] SQLAlchemy models
- [] Delta Lake schema definitions
- [] Kafka topic schemas
- [] Basic FastAPI application
- [] Structured logging with correlation IDs
- [] `.env.example` configuration

### Team Capacity
- **Solo Developer**: ~20-30 hours

---

## M1: Ingestion Layer (IN PROGRESS)

**Duration**: 2 weeks
**Goal**: Build reliable data connectors with fallback logic

### Deliverables
- [ ] Base connector framework with circuit breaker
- [ ] OilPriceAPI connector
- [ ] EIA API connector
- [ ] GDELT connector
- [ ] NewsAPI connector
- [ ] Kafka producer with retry logic
- [ ] Dead letter queue handling
- [ ] Data quality checks

### Tasks
```
- [ ] Create base connector class
- [ ] Implement OilPriceAPI fetcher
- [ ] Implement EIA fallback fetcher
- [ ] Implement yFinance emergency fallback
- [ ] Add retry with exponential backoff
- [ ] Configure Kafka producer
- [ ] Set up DLQ consumer
- [ ] Write unit tests
```

### Team Capacity
- **Solo Developer**: ~20-30 hours

---

## M2: Medallion Pipeline

**Duration**: 2 weeks
**Goal**: Implement Bronze → Silver → Gold transformations

### Deliverables
- [ ] Kafka consumers for each topic
- [ ] Bronze layer persistence to Delta Lake
- [ ] Silver layer transformations
- [ ] Gold layer aggregations
- [ ] Schema evolution support
- [ ] Backfill job for historical data

### Tasks
```
- [ ] Create Kafka consumer base class
- [ ] Implement oil prices consumer
- [ ] Implement geopolitical events consumer
- [ ] Build Bronze → Silver transformation
- [ ] Build Silver → Gold aggregation
- [ ] Configure Delta Lake optimization
- [ ] Create backfill script
- [ ] Write integration tests
```

### Team Capacity
- **Solo Developer**: ~30-40 hours

---

## M3: Storage & API

**Duration**: 2 weeks
**Goal**: Set up PostgreSQL metadata storage and FastAPI endpoints

### Deliverables
- [ ] PostgreSQL schema with migrations
- [ ] Redis caching layer
- [ ] FastAPI endpoints for all domains
- [ ] API authentication
- [ ] Rate limiting
- [ ] Query optimization

### Tasks
```
- [ ] Design PostgreSQL schema
- [ ] Create Alembic migrations
- [ ] Implement Redis cache service
- [ ] Build prices endpoints
- [ ] Build risk endpoints
- [ ] Build alerts endpoints
- [ ] Add API key authentication
- [ ] Configure rate limits
- [ ] Write endpoint tests
```

### Team Capacity
- **Solo Developer**: ~30-40 hours

---

## M4: Dashboard

**Duration**: 2 weeks
**Goal**: Create Streamlit operational dashboard

### Deliverables
- [ ] Price monitoring dashboard
- [ ] Risk heat map (basic)
- [ ] Alert management UI
- [ ] Ship tracking visualization
- [ ] Historical charts

### Tasks
```
- [ ] Set up Streamlit app structure
- [ ] Build price charts with Plotly
- [ ] Create risk score display
- [ ] Build alert management page
- [ ] Add ship position map (Folium)
- [ ] Create historical analysis view
- [ ] Add sidebar navigation
- [ ] Test dashboard flows
```

### Team Capacity
- **Solo Developer**: ~25-35 hours

---

## M5: Observability

**Duration**: 1-2 weeks
**Goal**: Set up monitoring, alerting, and health checks

### Deliverables
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Health check endpoints
- [ ] Alert dispatchers (email, Slack)
- [ ] Structured logging

### Tasks
```
- [ ] Add Prometheus metrics to API
- [ ] Create Grafana dashboard templates
- [ ] Implement /health endpoints
- [ ] Build alert dispatcher service
- [ ] Configure log aggregation
- [ ] Set up error tracking
```

### Team Capacity
- **Solo Developer**: ~15-20 hours

---

## M6: Testing & Launch

**Duration**: 1-2 weeks
**Goal**: Ensure quality and deploy to production

### Deliverables
- [ ] Unit test coverage > 80%
- [ ] Integration tests
- [ ] CI/CD pipeline
- [ ] Deployment documentation
- [ ] User documentation

### Tasks
```
- [ ] Write unit tests for schemas
- [ ] Write unit tests for connectors
- [ ] Write integration tests for API
- [ ] Set up GitHub Actions
- [ ] Configure Docker builds
- [ ] Write deployment guide
- [ ] Create API documentation
- [ ] Conduct load testing
```

### Team Capacity
- **Solo Developer**: ~25-30 hours

---

## Resource Allocation

### Solo Developer Time Budget

| Phase | Estimated Hours | Actual (Best Case) |
|-------|----------------|-------------------|
| M0 | 20-30 | 10-15 |
| M1 | 20-30 | 15-20 |
| M2 | 30-40 | 20-25 |
| M3 | 30-40 | 20-25 |
| M4 | 25-35 | 15-20 |
| M5 | 15-20 | 10-15 |
| M6 | 25-30 | 15-20 |
| **Total** | **165-225** | **105-140** |

### Dependencies Between Milestones

```
M0 (Foundation)
    ↓
M1 (Ingestion) ← requires M0
    ↓
M2 (Pipeline) ← requires M1
    ↓
M3 (Storage/API) ← requires M2
    ↓
M4 (Dashboard) ← requires M3
    ↓
M5 (Observability) ← runs parallel with M3-M4
    ↓
M6 (Testing/Launch) ← requires M1-M5
```

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API rate limits | High | Medium | Implement caching, use fallback sources |
| Data quality issues | Medium | High | Add validation, monitoring |
| Performance bottlenecks | Medium | Medium | Design for scale, use profiling |
| Scope creep | High | High | Stick to MVP, defer nice-to-haves |

---

## Definition of Done

Each milestone is complete when:

- [ ] All deliverables implemented
- [ ] Unit tests written and passing
- [ ] Code reviewed (self-review if solo)
- [ ] Documentation updated
- [ ] No critical bugs
- [ ] Deployed to staging environment

---

## Future Enhancements (Post-MVP)

- [ ] ML-based forecasting models
- [ ] Interactive geopolitical heat map
- [ ] Real ship tracking (AIS integration)
- [ ] Mobile application
- [ ] Multi-tenancy support
- [ ] Custom indicators
- [ ] Third-party integrations
