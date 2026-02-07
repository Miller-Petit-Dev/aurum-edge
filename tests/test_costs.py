"""
TEST: Trading Costs
"""
import pytest

from aurum_edge.backtest.costs import apply_costs

def test_cost_calculation():
    """Test cost calculation"""
    entry_price = 100.0
    exit_price = 102.0
    
    net_pnl, costs = apply_costs(entry_price, exit_price, direction='long')
    
    # Gross PnL should be 2.0
    gross_pnl = exit_price - entry_price
    assert abs(gross_pnl - 2.0) < 1e-6
    
    # Net PnL should be less than gross
    assert net_pnl < gross_pnl, "Net PnL should be less than gross after costs"
    
    # Costs should be positive
    assert costs['total_cost'] > 0, "Total cost should be positive"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
