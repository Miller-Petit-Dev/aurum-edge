"""Data transformations"""
import pandas as pd
from loguru import logger

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw data"""
    logger.info("Cleaning data...")
    df = df.copy()
    df = df.dropna()
    df = df.drop_duplicates()
    df = df.sort_index()
    logger.info(f"Cleaned data: {len(df)} rows remaining")
    return df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names"""
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    return df
