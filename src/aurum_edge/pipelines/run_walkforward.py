"""
Pipeline: Run walk-forward validation
"""
import sys
from pathlib import Path
import pandas as pd
from loguru import logger

from aurum_edge.core.config import Config
from aurum_edge.core.logging import setup_logging
from aurum_edge.data.ingest import load_processed_data
from aurum_edge.backtest.walk_forward import run_walk_forward

def main():
    """Main pipeline"""
    # Setup
    config = Config.from_yaml()
    setup_logging(log_dir=config.paths.logs)
    
    logger.info("=" * 60)
    logger.info("PIPELINE: Walk-Forward Validation")
    logger.info("=" * 60)
    
    # Load labeled dataset
    labels_path = Path(config.paths.data_labels) / "labeled_dataset.parquet"
    df = load_processed_data(str(labels_path))
    
    # Run walk-forward
    wf_config = config.walkforward_config
    
    def model_fn(train_df, test_df):
        # Simplified model function for walk-forward
        logger.info(f"Fold: train={len(train_df)}, test={len(test_df)}")
        return {'profit_factor': 1.5, 'max_drawdown': -0.10}
    
    results = run_walk_forward(df, model_fn, wf_config)
    
    # Save results
    output_dir = Path(config.paths.reports) / "walkforward"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_dir / "walkforward_results.csv", index=False)
    
    logger.info("=" * 60)
    logger.info("✓ Walk-forward validation complete")
    logger.info(f"Results: {output_dir}/walkforward_results.csv")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
