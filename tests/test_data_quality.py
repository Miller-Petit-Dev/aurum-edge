"""
TEST: Data Quality Checks
"""
import pytest
import pandas as pd
import numpy as np

from aurum_edge.data.validate import (
    check_missing_values,
    check_duplicates,
    check_outliers,
    check_monotonic_time,
    validate_ohlc_logic
)

def test_missing_values_detection():
    """Test missing value detection"""
    df = pd.DataFrame({
        'open': [100, 101, np.nan, 103],
        'close': [100, 101, 102, 103]
    })
    
    missing = check_missing_values(df)
    assert missing['open'] == 1, "Should detect 1 missing value in 'open'"
    assert missing['close'] == 0, "Should detect 0 missing values in 'close'"

def test_duplicate_detection():
    """Test duplicate row detection"""
    dates = pd.date_range('2024-01-01', periods=5, freq='5min')
    df = pd.DataFrame({
        'value': [1, 2, 2, 3, 4]
    }, index=dates)
    
    # Add duplicate row
    df = pd.concat([df, df.iloc[[2]]])
    
    dup_count = check_duplicates(df)
    assert dup_count == 1, f"Should detect 1 duplicate, found {dup_count}"

def test_monotonic_time():
    """Test time monotonicity check"""
    # Non-monotonic
    dates = pd.to_datetime(['2024-01-01 10:00', '2024-01-01 10:05', '2024-01-01 10:03'])
    df_bad = pd.DataFrame({'value': [1, 2, 3]}, index=dates)
    
    assert not check_monotonic_time(df_bad), "Should detect non-monotonic time"
    
    # Monotonic
    dates = pd.date_range('2024-01-01', periods=10, freq='5min')
    df_good = pd.DataFrame({'value': range(10)}, index=dates)
    
    assert check_monotonic_time(df_good), "Should pass for monotonic time"

def test_ohlc_logic():
    """Test OHLC validation logic"""
    df = pd.DataFrame({
        'open': [100, 101, 102],
        'high': [105, 106, 107],
        'low': [95, 96, 97],
        'close': [103, 104, 105]
    })
    
    errors = validate_ohlc_logic(df)
    assert len(errors) == 0, f"Valid OHLC should have no errors, got: {errors}"
    
    # Invalid: high < close
    df_bad = pd.DataFrame({
        'open': [100],
        'high': [98],  # Invalid
        'low': [95],
        'close': [102]
    })
    
    errors = validate_ohlc_logic(df_bad)
    assert len(errors) > 0, "Should detect invalid OHLC"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
