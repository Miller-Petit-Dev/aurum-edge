"""
Data quality validation
"""
from typing import Dict, List

import numpy as np
import pandas as pd
from loguru import logger


def check_missing_values(df: pd.DataFrame) -> Dict[str, int]:
    """Check for missing values"""
    missing = df.isnull().sum().to_dict()
    if any(v > 0 for v in missing.values()):
        logger.warning(f"Missing values found: {missing}")
    return missing


def check_duplicates(df: pd.DataFrame) -> int:
    """Check for duplicate rows"""
    dup_count = df.duplicated().sum()
    if dup_count > 0:
        logger.warning(f"Found {dup_count} duplicate rows")
    return dup_count


def check_outliers(df: pd.DataFrame, columns: List[str], threshold: float = 5.0) -> Dict[str, int]:
    """
    Check for outliers using z-score
    
    Args:
        df: DataFrame
        columns: Columns to check
        threshold: Z-score threshold (default 5.0)
    
    Returns:
        Dict of column -> outlier count
    """
    outliers = {}
    
    for col in columns:
        if col not in df.columns:
            continue
        
        z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
        outlier_count = (z_scores > threshold).sum()
        
        if outlier_count > 0:
            logger.warning(f"{col}: {outlier_count} outliers (z > {threshold})")
            outliers[col] = outlier_count
    
    return outliers


def check_monotonic_time(df: pd.DataFrame) -> bool:
    """Check if index is monotonically increasing"""
    is_monotonic = df.index.is_monotonic_increasing
    
    if not is_monotonic:
        logger.error("Time index is not monotonically increasing!")
    
    return is_monotonic


def validate_ohlc_logic(df: pd.DataFrame) -> List[str]:
    """
    Validate OHLC logic (high >= open/close, low <= open/close, etc.)
    
    Returns:
        List of validation errors
    """
    errors = []
    
    # High should be >= max(open, close)
    invalid_high = df['high'] < df[['open', 'close']].max(axis=1)
    if invalid_high.any():
        count = invalid_high.sum()
        errors.append(f"High < max(open, close): {count} rows")
    
    # Low should be <= min(open, close)
    invalid_low = df['low'] > df[['open', 'close']].min(axis=1)
    if invalid_low.any():
        count = invalid_low.sum()
        errors.append(f"Low > min(open, close): {count} rows")
    
    # High should be >= low
    invalid_range = df['high'] < df['low']
    if invalid_range.any():
        count = invalid_range.sum()
        errors.append(f"High < Low: {count} rows")
    
    if errors:
        for err in errors:
            logger.error(f"OHLC validation failed: {err}")
    
    return errors


def run_full_validation(df: pd.DataFrame, config: dict) -> bool:
    """
    Run full data validation suite
    
    Returns:
        True if all checks pass
    """
    logger.info("Running full data validation...")
    
    all_passed = True
    
    # Missing values
    missing = check_missing_values(df)
    if any(v > 0 for v in missing.values()):
        all_passed = False
    
    # Duplicates
    dup_count = check_duplicates(df)
    if dup_count > 0:
        all_passed = False
    
    # Outliers
    outlier_threshold = config.get('outlier_threshold', 5.0)
    outliers = check_outliers(df, ['open', 'high', 'low', 'close'], outlier_threshold)
    if outliers:
        all_passed = False
    
    # Monotonic time
    if not check_monotonic_time(df):
        all_passed = False
    
    # OHLC logic
    ohlc_errors = validate_ohlc_logic(df)
    if ohlc_errors:
        all_passed = False
    
    # Min rows
    min_rows = config.get('min_rows', 1000)
    if len(df) < min_rows:
        logger.error(f"Insufficient data: {len(df)} rows < {min_rows} required")
        all_passed = False
    
    if all_passed:
        logger.info("✓ All validation checks passed")
    else:
        logger.error("✗ Some validation checks failed")
    
    return all_passed
