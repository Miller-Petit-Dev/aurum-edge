# AURUM-EDGE v2: System Architecture

## Design Principles

1. **Separation of Concerns**: Data → Features → Labels → Model → Decision → Execution
2. **Fail-Safe Defaults**: Reject trades by default, require explicit approval
3. **Immutable Pipelines**: Each step produces versioned artifacts
4. **Observable Systems**: Log everything, monitor continuously
5. **Defensive Programming**: Validate inputs, handle errors, prevent catastrophe

## Module Structure

```
aurum_edge/
├── core/           # Config, logging, monitoring, time utils
├── data/           # Ingestion, validation, transforms, splits
├── features/       # Feature engineering with leakage guards
├── labeling/       # Triple-barrier and label validation
├── models/         # Training, tuning, calibration, registry, gating
├── backtest/       # Engine, metrics, walk-forward, costs
├── decision/       # Policy, expected value, signal generation
├── risk/           # Position sizing, limits, cooldown, kill switch
├── execution/      # Paper trading, human approval, MT5 bridge (phase 2)
└── pipelines/      # End-to-end workflows
```

## Data Flow

```
MT5 CSV Export
    ↓
[Ingest] → Raw Dataset
    ↓
[Validate] → Quality Checks
    ↓
[Transform] → Clean Dataset
    ↓
[Build Features] → Feature Dataset (with anti-leakage validation)
    ↓
[Label] → Triple Barrier Labels
    ↓
[Train] → Model (with tuning + calibration)
    ↓
[Walk-Forward] → Validation Results
    ↓
[Gating] → Promotion Decision
    ↓
[Deploy] → Production Model
    ↓
[Paper Trading] → Live Signals → [Human Approval] → Execution
```

## Anti-Leakage Architecture

**Critical**: Every transformation is checked for data leakage.

- Features use `shift(1)` or `rolling()` with `min_periods`
- No negative shifts allowed
- No future-looking operations
- Validation tests fail if leakage detected

## Gating System

Models must pass ALL gates to be promoted:

```python
{
    'min_profit_factor': 1.3,
    'max_drawdown': -0.15,
    'min_expectancy': 0.0,
    'min_trades': 50
}
```

If model fails, **previous model is retained**.

## Error Handling Strategy

1. **Data Errors**: Fail fast, log, alert
2. **Model Errors**: Fallback to previous model
3. **Execution Errors**: Reject trade, log, alert
4. **Risk Breaches**: Stop trading, require manual reset

## Monitoring Stack

- **Data Quality**: Check on every ingestion
- **Model Drift**: Track performance metrics over time
- **Execution Health**: Log all signals and fills
- **Risk Metrics**: Real-time position and exposure tracking

## Security Considerations

- API keys in environment variables (never in code)
- Model files versioned and backed up
- Trading logs immutable and auditable
- Human approval required for all real trades
