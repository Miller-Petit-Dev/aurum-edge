"""Return-based features"""
import pandas as pd

def add_return_features(df: pd.DataFrame, periods: list) -> pd.DataFrame:
    """Add return features for given periods"""
    for period in periods:
        df[f'return_{period}'] = df['close'].pct_change(period)
        df[f'log_return_{period}'] = pd.Series(index=df.index, data=0.0)
        mask = df['close'].shift(period) > 0
        df.loc[mask, f'log_return_{period}'] = (
            (df['close'] / df['close'].shift(period)).apply(lambda x: pd.Series.log(x) if x > 0 else 0)
        )
    return df
