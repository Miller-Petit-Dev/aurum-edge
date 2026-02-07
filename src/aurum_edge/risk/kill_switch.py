"""Kill switch for catastrophic losses"""
from loguru import logger

class KillSwitch:
    """Emergency stop for trading"""
    
    def __init__(self, config):
        self.config = config.get('kill_switch', {})
        self.activated = False
        self.reason = None
    
    def check(self, current_balance: float, initial_balance: float):
        """Check if kill switch should activate"""
        if self.activated:
            return True
        
        # Check drawdown
        max_dd = self.config.get('max_drawdown', -0.20)
        current_dd = (current_balance - initial_balance) / initial_balance
        
        if current_dd <= max_dd:
            self.activate(f"Max drawdown exceeded: {current_dd:.2%}")
            return True
        
        # Check max total loss
        max_loss = self.config.get('max_total_loss', -200.0)
        total_loss = current_balance - initial_balance
        
        if total_loss <= max_loss:
            self.activate(f"Max total loss exceeded: ${total_loss:.2f}")
            return True
        
        return False
    
    def activate(self, reason: str):
        """Activate kill switch"""
        self.activated = True
        self.reason = reason
        logger.critical(f"🚨 KILL SWITCH ACTIVATED: {reason}")
    
    def reset(self, manual_confirmation: bool = False):
        """Reset kill switch (requires manual confirmation)"""
        if not manual_confirmation:
            logger.error("Kill switch reset requires manual confirmation")
            return False
        
        self.activated = False
        self.reason = None
        logger.warning("Kill switch manually reset")
        return True
