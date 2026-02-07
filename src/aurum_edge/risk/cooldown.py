"""Cooldown periods after losses"""
from datetime import datetime, timedelta
from loguru import logger

class CooldownManager:
    """Manage cooldown periods"""
    
    def __init__(self, config):
        self.config = config.get('cooldown', {})
        self.cooldown_until = None
    
    def activate_cooldown(self, duration_seconds: int):
        """Activate cooldown period"""
        self.cooldown_until = datetime.now() + timedelta(seconds=duration_seconds)
        logger.warning(f"Cooldown activated until {self.cooldown_until}")
    
    def is_in_cooldown(self) -> bool:
        """Check if currently in cooldown"""
        if self.cooldown_until is None:
            return False
        
        if datetime.now() < self.cooldown_until:
            remaining = (self.cooldown_until - datetime.now()).total_seconds()
            logger.info(f"In cooldown: {remaining:.0f}s remaining")
            return True
        
        self.cooldown_until = None
        return False
