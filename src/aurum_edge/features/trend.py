"""Trend indicators"""
import pandas as pd

def add_trend_features(df: pd.DataFrame, ema_periods: list) -> pd.DataFrame:
    """Add trend features"""
    for period in ema_periods:
        df[f'ema_{period}'] = df['close'].ewm(span=period).mean()
    
    # MACD
    df['macd'] = df['close'].ewm(span=12).mean() - df['close'].ewm(span=26).mean()
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_hist'] = df['macd'] - df['macd_signal']
    
    return df
