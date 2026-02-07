"""Probability calibration"""
from sklearn.calibration import CalibratedClassifierCV
from sklearn.isotonic import IsotonicRegression
import numpy as np

def calibrate_probabilities(y_true, y_pred_proba, method='isotonic'):
    """
    Calibrate predicted probabilities
    
    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        method: 'isotonic' or 'sigmoid'
    
    Returns:
        Calibrated probabilities
    """
    if method == 'isotonic':
        calibrator = IsotonicRegression(out_of_bounds='clip')
        calibrated = calibrator.fit_transform(y_pred_proba, y_true)
    else:
        # Placeholder for sigmoid calibration
        calibrated = y_pred_proba
    
    return calibrated, calibrator
