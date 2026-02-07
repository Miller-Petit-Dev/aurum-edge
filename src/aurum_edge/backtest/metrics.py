"""Performance metrics"""
import numpy as np

def calculate_sharpe_ratio(returns, periods_per_year=252*288):
    """Calculate Sharpe ratio (annualized)"""
    if len(returns) == 0:
        return 0
    mean_return = returns.mean()
    std_return = returns.std()
    if std_return == 0:
        return 0
    sharpe = (mean_return / std_return) * np.sqrt(periods_per_year)
    return sharpe

def calculate_win_rate(trades):
    """Calculate win rate"""
    if len(trades) == 0:
        return 0
    wins = sum(1 for t in trades if t['pnl'] > 0)
    return wins / len(trades)
