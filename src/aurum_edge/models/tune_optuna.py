"""Hyperparameter tuning with Optuna"""
import optuna
import xgboost as xgb
from sklearn.metrics import log_loss
from loguru import logger

def optimize_xgboost(X_train, y_train, X_val, y_val, n_trials=30):
    """Optimize XGBoost hyperparameters"""
    
    def objective(trial):
        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
            'subsample': trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'seed': 42
        }
        
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dval = xgb.DMatrix(X_val, label=y_val)
        
        model = xgb.train(params, dtrain, num_boost_round=100)
        preds = model.predict(dval)
        loss = log_loss(y_val, preds)
        
        return loss
    
    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=n_trials)
    
    logger.info(f"Best params: {study.best_params}")
    logger.info(f"Best loss: {study.best_value}")
    
    return study.best_params
