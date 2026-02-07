# AURUM-EDGE v2: API Reference (Phase 2)

*This document will be expanded in Phase 2 when we add REST API endpoints for external integrations.*

## Planned Endpoints

### Model Management
- `GET /models` - List all models
- `GET /models/{model_id}` - Get model details
- `POST /models/train` - Trigger training
- `POST /models/promote` - Promote model to production

### Data Management
- `POST /data/ingest` - Ingest new data
- `GET /data/quality` - Get data quality report

### Trading
- `GET /signals` - Get recent signals
- `POST /signals/approve` - Approve a signal
- `GET /positions` - Get open positions
- `GET /history` - Get trade history

### Monitoring
- `GET /health` - System health check
- `GET /metrics` - Performance metrics
- `GET /alerts` - Active alerts

*Full OpenAPI spec to be provided in Phase 2.*
