"""Microstructure features"""
import pandas as pd
import numpy as np

def add_microstructure_features(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """Add microstructure features"""
    # Tick volume z-score
    if 'tick_volume' in df.columns or 'tickvolume' in df.columns:
        vol_col = 'tick_volume' if 'tick_volume' in df.columns else 'tickvolume'
        window = config.get('tick_volume_zscore_window', 20)
        df['tick_volume_zscore'] = (
            (df[vol_col] - df[vol_col].rolling(window).mean()) / 
            df[vol_col].rolling(window).std()
        )
    
    # Spread proxy
    if config.get('spread_proxy', True):
        df['spread_proxy'] = (df['high'] - df['low']) / df['close']
    
    # Price range ratio
    df['range_atr_ratio'] = (df['high'] - df['low']) / (df.get('atr_14', 1) + 1e-8)
    
    return df
