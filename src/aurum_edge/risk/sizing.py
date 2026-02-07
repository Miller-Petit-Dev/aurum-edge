"""Position sizing"""

def calculate_position_size(
    account_balance: float,
    risk_per_trade_pct: float,
    stop_loss_points: float,
    point_value: float = 0.1
) -> float:
    """
    Calculate position size based on risk
    
    Returns:
        Position size in lots
    """
    risk_amount = account_balance * risk_per_trade_pct
    position_size = risk_amount / (stop_loss_points * point_value)
    
    # Round to 0.01 lots
    position_size = round(position_size, 2)
    
    # Min/max limits
    position_size = max(0.01, min(position_size, 1.0))
    
    return position_size
