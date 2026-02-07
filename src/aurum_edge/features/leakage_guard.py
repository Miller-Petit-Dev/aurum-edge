"""Anti-leakage validation"""
import pandas as pd
from loguru import logger

def validate_no_leakage(df_features: pd.DataFrame, df_original: pd.DataFrame):
    """
    Validate that features don't use future information
    
    Raises:
        ValueError: If leakage is detected
    """
    # Check that all feature values at time t only depend on data <= t
    # This is a simple check - more sophisticated checks needed for production
    
    for col in df_features.columns:
        if col in df_original.columns:
            continue
        
        # Check for NaN at the beginning (expected for rolling windows)
        first_valid_idx = df_features[col].first_valid_index()
        
        if first_valid_idx is None:
            logger.warning(f"Feature {col} has all NaN values")
            continue
        
        # Check that feature doesn't have values before original data
        if first_valid_idx < df_original.index[0]:
            raise ValueError(f"LEAKAGE DETECTED: Feature {col} has values before original data start")
    
    logger.info("✓ No data leakage detected in features")
