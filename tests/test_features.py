"""
TEST: Feature Engineering
"""
import pytest
import pandas as pd
import numpy as np

from aurum_edge.features.returns import add_return_features
from aurum_edge.features.volatility import add_volatility_features

def test_return_features():
    """Test return calculation"""
    df = pd.DataFrame({
        'close': [100, 102, 101, 103, 105]
    })
    
    df = add_return_features(df, periods=[1])
    
    # Check return_1 calculation
    expected_return = (102 - 100) / 100
    assert abs(df['return_1'].iloc[1] - expected_return) < 1e-6, "Return calculation incorrect"

def test_volatility_features():
    """Test volatility features"""
    df = pd.DataFrame({
        'open': [100, 101, 102, 103, 104] * 10,
        'high': [102, 103, 104, 105, 106] * 10,
        'low': [99, 100, 101, 102, 103] * 10,
        'close': [101, 102, 103, 104, 105] * 10
    })
    
    df = add_volatility_features(df, windows=[10])
    
    # ATR should be calculated
    assert 'atr_14' in df.columns, "ATR should be calculated"
    assert df['atr_14'].notna().sum() > 0, "ATR should have values"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
