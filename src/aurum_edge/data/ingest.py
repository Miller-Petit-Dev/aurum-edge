"""
Data ingestion from CSV (MT5 exports)
"""
from pathlib import Path
from typing import Optional

import pandas as pd
from loguru import logger


def load_mt5_csv(
    filepath: str,
    date_col: str = "Date",
    time_col: str = "Time",
    columns_mapping: Optional[dict] = None
) -> pd.DataFrame:
    """
    Load MT5 exported CSV file
    
    Args:
        filepath: Path to CSV file
        date_col: Date column name
        time_col: Time column name
        columns_mapping: Optional column name mapping
    
    Returns:
        DataFrame with datetime index and OHLC columns
    """
    logger.info(f"Loading MT5 CSV from: {filepath}")
    
    # Read CSV
    df = pd.read_csv(filepath)
    
    logger.info(f"Loaded {len(df)} rows, columns: {list(df.columns)}")
    
    # Combine date and time
    if time_col in df.columns:
        df['datetime'] = pd.to_datetime(df[date_col] + ' ' + df[time_col])
    else:
        df['datetime'] = pd.to_datetime(df[date_col])
    
    # Set index
    df = df.set_index('datetime')
    df = df.sort_index()
    
    # Standardize column names
    if columns_mapping:
        df = df.rename(columns=columns_mapping)
    
    # Ensure lowercase column names
    df.columns = [c.lower() for c in df.columns]
    
    # Expected columns
    expected = ['open', 'high', 'low', 'close']
    missing = [c for c in expected if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    logger.info(f"Data range: {df.index[0]} to {df.index[-1]}")
    
    return df


def save_processed_data(df: pd.DataFrame, filepath: str):
    """Save processed data to parquet"""
    output_path = Path(filepath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df.to_parquet(filepath, compression='snappy')
    logger.info(f"Saved processed data to: {filepath}")


def load_processed_data(filepath: str) -> pd.DataFrame:
    """Load processed data from parquet"""
    df = pd.read_parquet(filepath)
    logger.info(f"Loaded processed data from: {filepath}")
    return df
