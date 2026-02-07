"""Decision policy (value trading)"""
import numpy as np
from loguru import logger

def apply_decision_policy(
    predictions: np.ndarray,
    threshold: float = 0.6,
    expected_values: np.ndarray = None
) -> np.ndarray:
    """
    Apply decision policy to model predictions
    
    Args:
        predictions: Predicted probabilities
        threshold: Minimum confidence threshold
        expected_values: Expected value of each trade (optional)
    
    Returns:
        Binary signals (1=trade, 0=no-trade)
    """
    signals = np.zeros(len(predictions))
    
    # Base threshold filter
    signals[predictions >= threshold] = 1
    
    # Expected value filter (if available)
    if expected_values is not None:
        signals[expected_values <= 0] = 0
    
    num_signals = signals.sum()
    logger.info(f"Generated {num_signals} signals from {len(predictions)} predictions ({num_signals/len(predictions)*100:.1f}%)")
    
    return signals

def calculate_expected_value(
    probability: float,
    avg_win: float,
    avg_loss: float
) -> float:
    """Calculate expected value of a trade"""
    ev = (probability * avg_win) + ((1 - probability) * avg_loss)
    return ev
