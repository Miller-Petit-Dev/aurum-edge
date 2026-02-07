"""
Triple Barrier Labeling Method
"""
import numpy as np
import pandas as pd
from loguru import logger

def apply_triple_barrier(
    df: pd.DataFrame,
    tp_multiplier: float = 2.0,
    sl_multiplier: float = 1.0,
    time_bars: int = 12,
    atr_col: str = 'atr_14'
) -> pd.DataFrame:
    """
    Apply triple barrier method for labeling
    
    Args:
        df: DataFrame with OHLC and ATR
        tp_multiplier: Take profit as multiple of ATR
        sl_multiplier: Stop loss as multiple of ATR
        time_bars: Maximum holding period in bars
        atr_col: ATR column name
    
    Returns:
        DataFrame with 'label' column added
    """
    logger.info(f"Applying triple barrier: TP={tp_multiplier}x ATR, SL={sl_multiplier}x ATR, Time={time_bars} bars")
    
    df = df.copy()
    df['label'] = -1  # Default: neutral
    
    for i in range(len(df) - time_bars):
        entry_price = df['close'].iloc[i]
        atr = df[atr_col].iloc[i]
        
        if pd.isna(atr) or atr == 0:
            continue
        
        tp_price = entry_price + (tp_multiplier * atr)
        sl_price = entry_price - (sl_multiplier * atr)
        
        # Look forward up to time_bars
        future_slice = df.iloc[i+1:i+1+time_bars]
        
        # Check which barrier hits first
        tp_hit = (future_slice['high'] >= tp_price).idxmax() if (future_slice['high'] >= tp_price).any() else None
        sl_hit = (future_slice['low'] <= sl_price).idxmax() if (future_slice['low'] <= sl_price).any() else None
        
        if tp_hit and sl_hit:
            # Both hit - which came first?
            tp_idx = future_slice.index.get_loc(tp_hit)
            sl_idx = future_slice.index.get_loc(sl_hit)
            
            if tp_idx < sl_idx:
                df.loc[df.index[i], 'label'] = 1  # TP hit first -> LONG
            else:
                df.loc[df.index[i], 'label'] = 0  # SL hit first -> SHORT/no-trade
        elif tp_hit:
            df.loc[df.index[i], 'label'] = 1
        elif sl_hit:
            df.loc[df.index[i], 'label'] = 0
        # else: time barrier hit (neutral) - already -1
    
    # Count labels
    label_counts = df['label'].value_counts()
    logger.info(f"Label distribution: {label_counts.to_dict()}")
    
    # Handle neutrals (MVP: drop them)
    df_labeled = df[df['label'] != -1].copy()
    logger.info(f"After removing neutrals: {len(df_labeled)} samples")
    
    return df_labeled

def balance_labels(df: pd.DataFrame, method: str = 'undersample') -> pd.DataFrame:
    """Balance class distribution"""
    label_counts = df['label'].value_counts()
    min_count = label_counts.min()
    
    if method == 'undersample':
        df_balanced = df.groupby('label').sample(n=min_count, random_state=42)
        df_balanced = df_balanced.sort_index()
        logger.info(f"Balanced dataset: {len(df_balanced)} samples")
        return df_balanced
    
    return df
