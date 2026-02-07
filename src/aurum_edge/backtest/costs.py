"""Trading costs simulation"""

def apply_costs(entry_price, exit_price, direction='long', config=None):
    """
    Apply trading costs to a trade
    
    Returns:
        Adjusted PnL after costs
    """
    if config is None:
        spread_points = 2.0
        slippage_points = 0.5
    else:
        spread_points = config.get('spread', {}).get('fixed_points', 2.0)
        slippage_points = config.get('slippage', {}).get('fixed_points', 0.5)
    
    # Convert points to price
    spread_cost = spread_points * 0.1
    slippage_cost = slippage_points * 0.1
    
    total_cost = spread_cost + slippage_cost
    
    # Gross PnL
    if direction == 'long':
        gross_pnl = exit_price - entry_price
    else:
        gross_pnl = entry_price - exit_price
    
    # Net PnL after costs
    net_pnl = gross_pnl - total_cost
    
    return net_pnl, {
        'spread_cost': spread_cost,
        'slippage_cost': slippage_cost,
        'total_cost': total_cost
    }
