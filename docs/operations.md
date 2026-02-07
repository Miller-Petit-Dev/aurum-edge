# AURUM-EDGE v2: Operations Guide

## Daily Workflow

### 1. Morning Routine (Before Market Open)

```bash
# Activate environment
cd ~/Documents/aurum-edge
source venv/bin/activate

# Export fresh data from MT5
# (See README for MT5 export instructions)

# Validate data quality
make validate-data

# Check system health
tail -n 50 logs/aurum_edge_*.log
```

### 2. Model Training (Weekly)

```bash
# Full pipeline
make build-dataset
make build-features
make build-labels
make train

# Review training report
cat reports/experiments/latest/summary.txt
```

### 3. Backtesting (After Model Update)

```bash
# Run walk-forward validation
make backtest

# Review results
cat reports/walkforward/summary.md
```

**Decision Point**: Does model pass gating? If NO, keep previous model.

### 4. Paper Trading (Continuous)

```bash
# Start paper trading
make paper

# Monitor logs in real-time
tail -f logs/aurum_edge_*.log
```

**Review signals as they arrive via Telegram/Discord.**

### 5. End of Day Review

```bash
# Generate daily report
python scripts/daily_report.py  # (Future: phase 2)

# Check:
# - Number of signals generated
# - Number approved/rejected
# - Paper P&L
# - Risk limit status
# - Any alerts or errors
```

## Weekly Tasks

- **Sunday**: Train fresh model on new data
- **Monday**: Validate model with walk-forward
- **Wednesday**: Review week-to-date performance
- **Friday**: Generate weekly summary report

## Monthly Tasks

- Review model registry and archive old models
- Analyze false positives and false negatives
- Update risk parameters if account size changed
- Review and update documentation

## Troubleshooting Runbook

### Data Issues

**Symptom**: "Validation FAILED" error

**Diagnosis**:
```bash
make validate-data
cat logs/aurum_edge_*.log | grep ERROR
```

**Solutions**:
- Check MT5 export format
- Verify CSV has all required columns
- Check for gaps in time series
- Look for extreme outliers

### Model Not Promoting

**Symptom**: Gating fails, model not deployed

**This is NORMAL if strategy has no edge!**

**Analysis**:
1. Review backtest metrics
2. Check label distribution (balanced?)
3. Verify costs are realistic
4. Look at win rate vs avg win/loss

**Do NOT**:
- Lower gating thresholds to force promotion
- Ignore poor backtest results
- Trade with failing model

### No Signals Generated

**Symptom**: Model produces no signals

**Diagnosis**:
- Check decision policy threshold (too high?)
- Review model predictions distribution
- Verify expected value calculations

**Solutions**:
- Adjust threshold (carefully)
- Retrain with different label parameters
- Check if market conditions changed

### Paper Trading Execution Errors

**Symptom**: Trades not executing in paper trading

**Diagnosis**:
```bash
grep "execution" logs/aurum_edge_*.log
```

**Solutions**:
- Check risk limits (daily loss hit?)
- Verify cooldown not active
- Check kill switch status
- Review human approval logs

## Emergency Procedures

### Kill Switch Activated

**Action**:
1. **STOP ALL ACTIVITY IMMEDIATELY**
2. Review what triggered kill switch
3. Analyze all trades that led to activation
4. Determine if bug, market event, or valid stop
5. Fix root cause
6. Reset kill switch ONLY with explicit confirmation

### Data Corruption Detected

**Action**:
1. Stop all pipelines
2. Backup current state
3. Re-export clean data from MT5
4. Validate thoroughly
5. Rebuild from scratch
6. Compare results with previous version

### Model Producing Nonsense

**Action**:
1. Rollback to previous model immediately
2. Review training logs
3. Check for data leakage
4. Verify feature engineering
5. Run full test suite
6. Retrain with validation

## Best Practices

1. **Never skip validation** - It exists for a reason
2. **Trust the gating** - If model doesn't pass, don't use it
3. **Log everything** - Future you will thank present you
4. **Review regularly** - Don't set-and-forget
5. **Update docs** - Keep operations guide current
6. **Back up everything** - Models, data, configs
7. **Test in paper first** - Always, no exceptions
8. **Respect risk limits** - They protect your capital
9. **Human approval matters** - Don't rubber-stamp
10. **When in doubt, don't trade** - Preservation > profits

## Support Escalation

Level 1: Check logs and this operations guide
Level 2: Review architecture and thesis docs
Level 3: Contact LIA Engineering Solutions
Level 4: Stop trading, manual investigation required
