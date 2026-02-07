"""Volatility features"""
import pandas as pd
import numpy as np

def add_volatility_features(df: pd.DataFrame, windows: list) -> pd.DataFrame:
    """Add volatility features"""
    # ATR
    df['tr'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift(1)),
            abs(df['low'] - df['close'].shift(1))
        )
    )
    df['atr_14'] = df['tr'].rolling(14).mean()
    
    # Rolling volatility
    for window in windows:
        df[f'volatility_{window}'] = df['close'].pct_change().rolling(window).std()
    
    return df
