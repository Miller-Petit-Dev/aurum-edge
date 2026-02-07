"""Paper trading simulator"""
from dataclasses import dataclass
from datetime import datetime
from loguru import logger

@dataclass
class PaperTrade:
    """Paper trade record"""
    entry_time: datetime
    entry_price: float
    direction: str  # 'long' or 'short'
    size: float
    stop_loss: float
    take_profit: float
    exit_time: datetime = None
    exit_price: float = None
    pnl: float = 0.0
    status: str = 'open'

class PaperTradingEngine:
    """Simulate real trading without real money"""
    
    def __init__(self, initial_balance=1000.0):
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.trades = []
        self.open_trades = []
    
    def execute_trade(
        self,
        entry_price: float,
        direction: str,
        size: float,
        stop_loss: float,
        take_profit: float
    ):
        """Execute a paper trade"""
        trade = PaperTrade(
            entry_time=datetime.now(),
            entry_price=entry_price,
            direction=direction,
            size=size,
            stop_loss=stop_loss,
            take_profit=take_profit
        )
        
        self.open_trades.append(trade)
        logger.info(f"Paper trade opened: {direction} @ {entry_price:.2f}")
        
        return trade
    
    def close_trade(self, trade: PaperTrade, exit_price: float):
        """Close a paper trade"""
        trade.exit_time = datetime.now()
        trade.exit_price = exit_price
        
        if trade.direction == 'long':
            trade.pnl = (exit_price - trade.entry_price) * trade.size
        else:
            trade.pnl = (trade.entry_price - exit_price) * trade.size
        
        trade.status = 'closed'
        self.balance += trade.pnl
        
        self.open_trades.remove(trade)
        self.trades.append(trade)
        
        logger.info(f"Paper trade closed: PnL ${trade.pnl:.2f}, Balance ${self.balance:.2f}")
        
        return trade
    
    def get_summary(self):
        """Get trading summary"""
        return {
            'initial_balance': self.initial_balance,
            'current_balance': self.balance,
            'total_pnl': self.balance - self.initial_balance,
            'num_trades': len(self.trades),
            'open_trades': len(self.open_trades)
        }
