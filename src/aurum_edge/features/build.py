"""Main feature building orchestrator"""
import pandas as pd
from loguru import logger

from aurum_edge.features.returns import add_return_features
from aurum_edge.features.volatility import add_volatility_features
from aurum_edge.features.trend import add_trend_features
from aurum_edge.features.session import add_session_features
from aurum_edge.features.microstructure import add_microstructure_features
from aurum_edge.features.leakage_guard import validate_no_leakage

def build_all_features(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Build all features for the dataset
    
    Args:
        df: DataFrame with OHLC data
        config: Feature configuration
    
    Returns:
        DataFrame with features added
    """
    logger.info("Building features...")
    
    df_features = df.copy()
    
    # Returns
    df_features = add_return_features(df_features, config.get('returns_periods', [1, 3, 5]))
    
    # Volatility
    df_features = add_volatility_features(df_features, config.get('volatility_windows', [10, 20]))
    
    # Trend
    df_features = add_trend_features(df_features, config.get('ema_periods', [9, 21, 50]))
    
    # Session
    if config.get('session_splits', True):
        df_features = add_session_features(df_features)
    
    # Microstructure
    df_features = add_microstructure_features(df_features, config)
    
    # Validate no leakage
    if config.get('validate_on_build', True):
        validate_no_leakage(df_features, df)
    
    logger.info(f"Features built: {len(df_features.columns)} total columns")
    
    return df_features
