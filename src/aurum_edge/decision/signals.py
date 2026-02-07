"""Signal generation"""
import pandas as pd

def generate_signals(predictions, policy_config):
    """Generate trading signals from model predictions"""
    threshold = policy_config.get('threshold', 0.6)
    
    signals = pd.Series(index=predictions.index, data=0)
    signals[predictions >= threshold] = 1
    
    return signals
