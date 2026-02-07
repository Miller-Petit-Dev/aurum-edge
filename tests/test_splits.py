"""
TEST: Temporal Split Validation
Ensure train/test splits don't leak data across time
"""
import pytest
import pandas as pd
import numpy as np

from aurum_edge.data.split import train_test_split_temporal, get_walk_forward_splits

def test_temporal_split_no_overlap():
    """Test that train and test sets don't overlap"""
    dates = pd.date_range('2024-01-01', periods=1000, freq='5min')
    df = pd.DataFrame({'value': np.random.randn(1000)}, index=dates)
    
    train, test = train_test_split_temporal(df, test_size=0.2, purge_bars=5, embargo_bars=5)
    
    # Check no overlap
    assert train.index[-1] < test.index[0], "Train and test sets overlap!"
    
    # Check gap
    train_end = train.index[-1]
    test_start = test.index[0]
    gap_bars = len(df[(df.index > train_end) & (df.index < test_start)])
    assert gap_bars >= 10, f"Insufficient gap between train/test: {gap_bars} bars"
    
    print(f"✓ Temporal split validated: gap = {gap_bars} bars")

def test_walk_forward_splits_sequential():
    """Test that walk-forward splits are sequential"""
    dates = pd.date_range('2024-01-01', periods=5000, freq='5min')
    df = pd.DataFrame({'value': np.random.randn(5000)}, index=dates)
    
    splits = get_walk_forward_splits(df, train_months=1, test_weeks=1, step_weeks=1)
    
    # Check each split
    for i, (train, test) in enumerate(splits):
        # Train comes before test
        assert train.index[-1] < test.index[0], f"Fold {i}: train doesn't come before test"
        
        # If not last fold, check next fold starts after this test
        if i < len(splits) - 1:
            next_train = splits[i+1][0]
            assert test.index[0] <= next_train.index[0], f"Fold {i}: splits not sequential"
    
    print(f"✓ Walk-forward splits validated: {len(splits)} folds")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
