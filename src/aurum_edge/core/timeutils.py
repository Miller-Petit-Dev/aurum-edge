"""
Time utilities for financial data
"""
from datetime import datetime, timedelta
from typing import List, Tuple

import pandas as pd
import pytz


def ensure_utc(dt: pd.Timestamp) -> pd.Timestamp:
    """Ensure timestamp is UTC"""
    if dt.tz is None:
        return dt.tz_localize('UTC')
    return dt.tz_convert('UTC')


def get_session(timestamp: pd.Timestamp) -> str:
    """
    Get trading session for a timestamp
    
    Returns: 'asian', 'london', or 'newyork'
    """
    hour = timestamp.hour
    
    if 0 <= hour < 8:
        return 'asian'
    elif 8 <= hour < 13:
        return 'london'
    elif 13 <= hour < 21:
        return 'newyork'
    else:
        return 'asian'


def check_gaps(df: pd.DataFrame, max_gap_minutes: int = 15) -> List[Tuple]:
    """
    Check for gaps in time series data
    
    Returns: List of (start_time, end_time, gap_minutes) tuples
    """
    gaps = []
    diffs = df.index.to_series().diff()
    
    for idx, diff in diffs.items():
        if pd.notna(diff) and diff.total_seconds() > max_gap_minutes * 60:
            gap_minutes = diff.total_seconds() / 60
            gaps.append((idx - diff, idx, gap_minutes))
    
    return gaps


def resample_ohlc(df: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    """
    Resample OHLC data to different timeframe
    
    Args:
        df: DataFrame with OHLC columns
        timeframe: Target timeframe ('5T', '15T', '1H', etc.)
    """
    agg_dict = {
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
    }
    
    # Add volume if exists
    if 'volume' in df.columns:
        agg_dict['volume'] = 'sum'
    if 'tick_volume' in df.columns:
        agg_dict['tick_volume'] = 'sum'
    
    resampled = df.resample(timeframe).agg(agg_dict)
    return resampled.dropna()
