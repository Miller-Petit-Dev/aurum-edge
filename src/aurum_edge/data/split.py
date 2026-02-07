"""Temporal data splits (anti-leakage)"""
from typing import List, Tuple
import pandas as pd
from loguru import logger

def train_test_split_temporal(
    df: pd.DataFrame,
    test_size: float = 0.2,
    purge_bars: int = 0,
    embargo_bars: int = 0
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Temporal train/test split with purge and embargo
    
    Args:
        df: DataFrame with datetime index
        test_size: Fraction for test set
        purge_bars: Bars to remove after train set
        embargo_bars: Bars to remove at start of test set
    """
    n = len(df)
    split_idx = int(n * (1 - test_size))
    
    train_end = split_idx - purge_bars
    test_start = split_idx + embargo_bars
    
    train = df.iloc[:train_end]
    test = df.iloc[test_start:]
    
    logger.info(f"Train: {len(train)} rows, Test: {len(test)} rows")
    logger.info(f"Purged: {purge_bars} bars, Embargoed: {embargo_bars} bars")
    
    return train, test

def get_walk_forward_splits(
    df: pd.DataFrame,
    train_months: int = 3,
    test_weeks: int = 2,
    step_weeks: int = 2
) -> List[Tuple[pd.DataFrame, pd.DataFrame]]:
    """Generate walk-forward splits"""
    from dateutil.relativedelta import relativedelta
    
    splits = []
    start_date = df.index[0]
    end_date = df.index[-1]
    
    current_date = start_date
    
    while True:
        train_start = current_date
        train_end = current_date + relativedelta(months=train_months)
        test_start = train_end
        test_end = test_start + relativedelta(weeks=test_weeks)
        
        if test_end > end_date:
            break
        
        train_mask = (df.index >= train_start) & (df.index < train_end)
        test_mask = (df.index >= test_start) & (df.index < test_end)
        
        train_df = df[train_mask]
        test_df = df[test_mask]
        
        if len(train_df) > 0 and len(test_df) > 0:
            splits.append((train_df, test_df))
        
        current_date = current_date + relativedelta(weeks=step_weeks)
    
    logger.info(f"Generated {len(splits)} walk-forward splits")
    return splits
