# AURUM-EDGE v2: Thesis and Strategy Fundamentals

## Core Hypothesis

Machine learning can identify profitable trading opportunities in NAS100 M5 data **if and only if**:
1. Features capture genuine market microstructure
2. Labels reflect actual tradeable outcomes (accounting for costs)
3. Validation prevents overfitting to historical noise
4. Risk management prevents catastrophic losses
5. Execution costs are modeled realistically

## Why Triple-Barrier Labeling?

Traditional classification: "Will price go up or down?"
**Problem**: Ignores magnitude, time horizon, and transaction costs.

Triple-barrier method:
- **Take Profit (TP)**: Exit if price moves +X in our favor
- **Stop Loss (SL)**: Exit if price moves -Y against us
- **Time**: Exit after N bars if neither TP/SL hit

**Label = whichever barrier hits first**

This creates labels that reflect actual trading outcomes, not just directional movement.

## Why Walk-Forward Validation?

Cross-validation assumes IID (independent, identically distributed) data.
Financial time series violate this assumption.

Walk-forward:
- Train on period T1
- Test on future period T2
- Step forward, repeat
- **No peeking into future**

## Why Expected Value Trading?

Not all high-probability trades are good trades.

EV = (Win Probability × Avg Win) - (Loss Probability × Avg Loss) - Costs

We only trade when EV > 0, even if model confidence is high.

## Why Risk Management First?

A profitable strategy without risk management is a ticking time bomb.

Key protections:
- Daily loss limits (survive bad days)
- Position sizing (control risk per trade)
- Cooldown periods (prevent tilt)
- Kill switch (catastrophic stop)

## Why Human-in-the-Loop?

Algorithms don't understand:
- News events
- Market structure changes
- Black swan events
- Their own limitations

Human oversight prevents automated destruction of capital.

## References

- *Advances in Financial Machine Learning* - Marcos López de Prado
- *Evidence-Based Technical Analysis* - David Aronson
- *Quantitative Trading* - Ernest Chan
