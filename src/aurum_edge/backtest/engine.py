"""Backtest engine"""
import pandas as pd
import numpy as np
from loguru import logger

class BacktestEngine:
    """Simple backtest engine"""
    
    def __init__(self, initial_balance=1000.0, position_size=0.01):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.position_size = position_size
        self.trades = []
        self.equity_curve = []
    
    def run(self, signals: pd.DataFrame, prices: pd.DataFrame):
        """
        Run backtest
        
        Args:
            signals: DataFrame with 'signal' column (1=long, 0=short/no-trade)
            prices: DataFrame with OHLC prices
        """
        logger.info("Running backtest...")
        
        for i in range(len(signals)):
            signal = signals['signal'].iloc[i]
            entry_price = prices['close'].iloc[i]
            
            if signal == 1:
                # Simulate long trade
                exit_idx = min(i + 12, len(prices) - 1)  # 12 bar max hold
                exit_price = prices['close'].iloc[exit_idx]
                
                pnl = (exit_price - entry_price) * self.position_size
                self.balance += pnl
                
                self.trades.append({
                    'entry_time': prices.index[i],
                    'exit_time': prices.index[exit_idx],
                    'entry_price': entry_price,
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'return_pct': (exit_price - entry_price) / entry_price
                })
            
            self.equity_curve.append(self.balance)
        
        logger.info(f"Backtest complete: {len(self.trades)} trades")
        return self.get_metrics()
    
    def get_metrics(self):
        """Calculate performance metrics"""
        if not self.trades:
            return {}
        
        df_trades = pd.DataFrame(self.trades)
        
        total_pnl = df_trades['pnl'].sum()
        wins = df_trades[df_trades['pnl'] > 0]
        losses = df_trades[df_trades['pnl'] < 0]
        
        metrics = {
            'total_pnl': total_pnl,
            'num_trades': len(self.trades),
            'win_rate': len(wins) / len(self.trades) if len(self.trades) > 0 else 0,
            'avg_win': wins['pnl'].mean() if len(wins) > 0 else 0,
            'avg_loss': losses['pnl'].mean() if len(losses) > 0 else 0,
            'profit_factor': abs(wins['pnl'].sum() / losses['pnl'].sum()) if len(losses) > 0 and losses['pnl'].sum() != 0 else 0,
            'max_drawdown': self._calculate_max_drawdown(),
            'expectancy': df_trades['pnl'].mean()
        }
        
        return metrics
    
    def _calculate_max_drawdown(self):
        """Calculate maximum drawdown"""
        if not self.equity_curve:
            return 0
        
        equity = np.array(self.equity_curve)
        running_max = np.maximum.accumulate(equity)
        drawdown = (equity - running_max) / running_max
        return drawdown.min()
