"""
Pipeline: Build features from clean dataset
"""
import sys
from pathlib import Path
from loguru import logger

from aurum_edge.core.config import Config
from aurum_edge.core.logging import setup_logging
from aurum_edge.data.ingest import load_processed_data, save_processed_data
from aurum_edge.features.build import build_all_features

def main():
    """Main pipeline"""
    # Setup
    config = Config.from_yaml()
    setup_logging(log_dir=config.paths.logs)
    
    logger.info("=" * 60)
    logger.info("PIPELINE: Build Features")
    logger.info("=" * 60)
    
    # Load clean dataset
    dataset_path = Path(config.paths.data_processed) / "dataset_clean.parquet"
    
    if not dataset_path.exists():
        logger.error(f"Dataset not found: {dataset_path}")
        logger.error("Run 'make build-dataset' first")
        sys.exit(1)
    
    df = load_processed_data(str(dataset_path))
    
    # Build features
    feature_config = config.__dict__.get('features', {})
    df_features = build_all_features(df, feature_config)
    
    # Save
    output_path = Path(config.paths.data_features) / "features.parquet"
    save_processed_data(df_features, str(output_path))
    
    logger.info("=" * 60)
    logger.info("✓ Features built successfully")
    logger.info(f"Output: {output_path}")
    logger.info(f"Features: {len(df_features.columns)} columns")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
