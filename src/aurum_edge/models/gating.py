"""Model gating (promotion criteria)"""
from loguru import logger

def should_promote_model(metrics: dict, thresholds: dict) -> bool:
    """
    Determine if model should be promoted to production
    
    Args:
        metrics: Model performance metrics
        thresholds: Minimum acceptable metrics
    
    Returns:
        True if model passes all gates
    """
    gates_passed = []
    gates_failed = []
    
    # Check profit factor
    if metrics.get('profit_factor', 0) >= thresholds.get('min_profit_factor', 1.3):
        gates_passed.append('profit_factor')
    else:
        gates_failed.append(f"profit_factor: {metrics.get('profit_factor', 0):.2f} < {thresholds.get('min_profit_factor', 1.3)}")
    
    # Check drawdown
    if metrics.get('max_drawdown', -1) >= thresholds.get('max_drawdown', -0.15):
        gates_passed.append('max_drawdown')
    else:
        gates_failed.append(f"max_drawdown: {metrics.get('max_drawdown', -1):.2%}")
    
    # Check expectancy
    if metrics.get('expectancy', -999) > thresholds.get('min_expectancy', 0):
        gates_passed.append('expectancy')
    else:
        gates_failed.append(f"expectancy: {metrics.get('expectancy', -999):.2f}")
    
    # Check min trades
    if metrics.get('num_trades', 0) >= thresholds.get('min_trades', 50):
        gates_passed.append('num_trades')
    else:
        gates_failed.append(f"num_trades: {metrics.get('num_trades', 0)} < {thresholds.get('min_trades', 50)}")
    
    passed = len(gates_failed) == 0
    
    if passed:
        logger.info(f"✓ Model PASSED gating. Gates passed: {gates_passed}")
    else:
        logger.warning(f"✗ Model FAILED gating. Failed: {gates_failed}")
    
    return passed
