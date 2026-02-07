"""
Pipeline: Train model with tuning and calibration
"""
import sys
from pathlib import Path
import pandas as pd
from loguru import logger

from aurum_edge.core.config import Config
from aurum_edge.core.logging import setup_logging
from aurum_edge.data.ingest import load_processed_data
from aurum_edge.models.train import train_xgboost, save_model
from aurum_edge.models.tune_optuna import optimize_xgboost
from aurum_edge.models.calibrate import calibrate_probabilities
from aurum_edge.models.registry import ModelRegistry

def main():
    """Main pipeline"""
    # Setup
    config = Config.from_yaml()
    setup_logging(log_dir=config.paths.logs)
    
    logger.info("=" * 60)
    logger.info("PIPELINE: Train Model")
    logger.info("=" * 60)
    
    # Load labeled dataset
    labels_path = Path(config.paths.data_labels) / "labeled_dataset.parquet"
    
    if not labels_path.exists():
        logger.error(f"Labels not found: {labels_path}")
        logger.error("Run 'make build-labels' first")
        sys.exit(1)
    
    df = load_processed_data(str(labels_path))
    
    # Prepare X, y
    feature_cols = [c for c in df.columns if c not in ['label', 'date', 'time']]
    X = df[feature_cols].fillna(0)
    y = df['label']
    
    logger.info(f"Training data: {len(X)} samples, {len(feature_cols)} features")
    
    # Split train/val
    from sklearn.model_selection import train_test_split
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Hyperparameter tuning
    tuning_config = config.model.tuning
    if tuning_config.get('enabled', True):
        logger.info("Running hyperparameter optimization...")
        best_params = optimize_xgboost(
            X_train, y_train, X_val, y_val,
            n_trials=tuning_config.get('n_trials', 30)
        )
    else:
        best_params = {
            'objective': 'binary:logistic',
            'max_depth': 6,
            'learning_rate': 0.1
        }
    
    # Train final model
    logger.info("Training final model...")
    model = train_xgboost(X_train, y_train, params=best_params)
    
    # Save model
    model_path = Path(config.paths.models) / "model_latest.xgb"
    save_model(model, str(model_path))
    
    # Register model
    registry = ModelRegistry(registry_dir=str(Path(config.paths.models) / "registry"))
    registry.register_model("latest", {
        'path': str(model_path),
        'params': best_params,
        'n_features': len(feature_cols),
        'train_samples': len(X_train)
    })
    
    logger.info("=" * 60)
    logger.info("✓ Model training complete")
    logger.info(f"Model saved: {model_path}")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
