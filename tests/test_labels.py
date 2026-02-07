"""
TEST: Label Generation Validation
"""
import pytest
import pandas as pd
import numpy as np

from aurum_edge.labeling.triple_barrier import apply_triple_barrier

def test_triple_barrier_labels():
    """Test triple barrier labeling"""
    # Create sample data with ATR
    dates = pd.date_range('2024-01-01', periods=200, freq='5min')
    df = pd.DataFrame({
        'open': np.random.randn(200).cumsum() + 100,
        'high': np.random.randn(200).cumsum() + 102,
        'low': np.random.randn(200).cumsum() + 98,
        'close': np.random.randn(200).cumsum() + 100,
        'atr_14': np.full(200, 2.0)  # Fixed ATR for simplicity
    }, index=dates)
    
    # Apply triple barrier
    df_labeled = apply_triple_barrier(df, tp_multiplier=2.0, sl_multiplier=1.0, time_bars=12)
    
    # Check label values
    unique_labels = df_labeled['label'].unique()
    assert all(label in [0, 1] for label in unique_labels), f"Invalid labels found: {unique_labels}"
    
    # Check we have labels
    assert len(df_labeled) > 0, "No labels generated"
    
    print(f"✓ Triple barrier labels validated: {len(df_labeled)} samples")

def test_label_distribution():
    """Test that label distribution is reasonable"""
    dates = pd.date_range('2024-01-01', periods=500, freq='5min')
    df = pd.DataFrame({
        'open': np.random.randn(500).cumsum() + 100,
        'high': np.random.randn(500).cumsum() + 102,
        'low': np.random.randn(500).cumsum() + 98,
        'close': np.random.randn(500).cumsum() + 100,
        'atr_14': np.full(500, 2.0)
    }, index=dates)
    
    df_labeled = apply_triple_barrier(df)
    
    label_counts = df_labeled['label'].value_counts()
    total = len(df_labeled)
    
    # Check each class has at least 5% of samples
    for label, count in label_counts.items():
        pct = count / total
        assert pct >= 0.05, f"Class {label} has only {pct:.1%} of samples"
    
    print(f"✓ Label distribution validated")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
