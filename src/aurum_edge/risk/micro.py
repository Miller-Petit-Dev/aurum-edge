"""Risk management for micro accounts"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from loguru import logger

@dataclass
class RiskLimits:
    """Risk limit tracking"""
    daily_loss_limit: float
    max_daily_loss: float = 0.0
    max_trades_per_day: int = 5
    trades_today: int = 0
    consecutive_losses: int = 0
    last_reset: datetime = None
    
    def reset_daily(self):
        """Reset daily counters"""
        self.max_daily_loss = 0.0
        self.trades_today = 0
        self.last_reset = datetime.now()
        logger.info("Daily risk limits reset")
    
    def record_trade(self, pnl: float):
        """Record a trade result"""
        self.trades_today += 1
        self.max_daily_loss += pnl
        
        if pnl < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
    
    def can_trade(self) -> bool:
        """Check if trading is allowed"""
        # Check daily loss
        if self.max_daily_loss <= self.daily_loss_limit:
            logger.warning(f"Daily loss limit reached: {self.max_daily_loss}")
            return False
        
        # Check max trades
        if self.trades_today >= self.max_trades_per_day:
            logger.warning(f"Max trades per day reached: {self.trades_today}")
            return False
        
        return True

class RiskManager:
    """Manage risk limits"""
    
    def __init__(self, config):
        self.limits = RiskLimits(
            daily_loss_limit=config.get('daily_limits', {}).get('max_daily_loss', -100.0),
            max_trades_per_day=config.get('daily_limits', {}).get('max_trades_per_day', 5)
        )
    
    def check_and_update(self, trade_pnl: float = None):
        """Check limits and update if trade executed"""
        if trade_pnl is not None:
            self.limits.record_trade(trade_pnl)
        
        return self.limits.can_trade()
