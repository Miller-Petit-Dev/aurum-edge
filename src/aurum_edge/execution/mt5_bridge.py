"""
MetaTrader 5 Bridge (FASE 2 - NO USAR EN MVP)

ADVERTENCIA: Este módulo NO debe usarse con dinero real sin:
1. Validación exhaustiva en demo
2. Aprobación explícita de human-in-the-loop
3. Límites de riesgo estrictos configurados
"""
from loguru import logger

class MT5Bridge:
    """Bridge to MetaTrader 5 (Phase 2 only)"""
    
    def __init__(self, config):
        self.config = config
        self.enabled = config.get('real_trading', {}).get('enabled', False)
        
        if self.enabled:
            logger.critical("⚠️  MT5 REAL TRADING IS ENABLED - THIS IS DANGEROUS!")
            logger.critical("⚠️  Ensure you have validated EVERYTHING in demo first!")
        else:
            logger.info("MT5 bridge initialized in DISABLED mode (safe)")
    
    def connect(self):
        """Connect to MT5 terminal"""
        if not self.enabled:
            logger.warning("MT5 bridge is disabled - cannot connect")
            return False
        
        logger.critical("MT5 connection - NOT IMPLEMENTED IN MVP")
        return False
    
    def send_order(self, order_params):
        """Send order to MT5"""
        if not self.enabled:
            logger.error("MT5 bridge is disabled - rejecting order")
            return None
        
        logger.critical("⚠️  REAL ORDER ATTEMPT - BLOCKED IN MVP")
        raise NotImplementedError("MT5 real trading not implemented in MVP - use paper trading")
    
    def get_positions(self):
        """Get open positions from MT5"""
        if not self.enabled:
            return []
        
        logger.warning("MT5 positions - not implemented")
        return []
