"""Session-based features"""
import pandas as pd

def add_session_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add session indicators"""
    hour = df.index.hour
    
    df['session_asian'] = ((hour >= 0) & (hour < 8)).astype(int)
    df['session_london'] = ((hour >= 8) & (hour < 13)).astype(int)
    df['session_newyork'] = ((hour >= 13) & (hour < 21)).astype(int)
    
    return df
