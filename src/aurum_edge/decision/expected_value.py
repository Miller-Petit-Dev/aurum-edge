"""Expected value calculations"""

def compute_ev_threshold(win_rate, avg_win, avg_loss):
    """Compute EV-based probability threshold"""
    # EV = p*W + (1-p)*L = 0
    # Solve for p: p = -L / (W - L)
    if avg_win == avg_loss:
        return 0.5
    threshold = abs(avg_loss) / (avg_win + abs(avg_loss))
    return threshold
