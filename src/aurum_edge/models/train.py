"""Model training with XGBoost"""
import joblib
from pathlib import Path
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from loguru import logger

def train_xgboost(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    params: dict = None,
    num_boost_round: int = 100
) -> xgb.Booster:
    """Train XGBoost model"""
    if params is None:
        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'max_depth': 6,
            'learning_rate': 0.1,
            'seed': 42
        }
    
    dtrain = xgb.DMatrix(X_train, label=y_train)
    
    logger.info(f"Training XGBoost with {len(X_train)} samples...")
    model = xgb.train(params, dtrain, num_boost_round=num_boost_round)
    
    return model

def save_model(model, filepath: str):
    """Save model to disk"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    model.save_model(filepath)
    logger.info(f"Model saved to {filepath}")

def load_model(filepath: str) -> xgb.Booster:
    """Load model from disk"""
    model = xgb.Booster()
    model.load_model(filepath)
    logger.info(f"Model loaded from {filepath}")
    return model
