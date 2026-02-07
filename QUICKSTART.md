# Quickstart - AURUM-EDGE v2

## 30-Second Setup

```bash
cd aurum-edge
make setup
make test
```

## Export Data from MT5

1. Open MetaTrader 5
2. Press F2 (History Center)
3. Select NAS100 → M5
4. Click "Export"
5. Save as `data/raw/nas100_m5.csv`

## Run Complete Pipeline

```bash
make build-dataset
make build-features
make build-labels
make train
make backtest
```

## Start Paper Trading

```bash
make paper
```

Check logs in real-time:
```bash
tail -f logs/aurum_edge_*.log
```

## Next Steps

- Read `docs/operations.md` for daily workflow
- Configure Telegram bot (optional) - see README
- Review `docs/thesis.md` to understand the strategy

