"""
Pipeline: Build labels using triple barrier
"""
import sys
from pathlib import Path
from loguru import logger

from aurum_edge.core.config import Config
from aurum_edge.core.logging import setup_logging
from aurum_edge.data.ingest import load_processed_data, save_processed_data
from aurum_edge.labeling.triple_barrier import apply_triple_barrier

def main():
    """Main pipeline"""
    # Setup
    config = Config.from_yaml()
    setup_logging(log_dir=config.paths.logs)
    
    logger.info("=" * 60)
    logger.info("PIPELINE: Build Labels")
    logger.info("=" * 60)
    
    # Load features
    features_path = Path(config.paths.data_features) / "features.parquet"
    
    if not features_path.exists():
        logger.error(f"Features not found: {features_path}")
        logger.error("Run 'make build-features' first")
        sys.exit(1)
    
    df = load_processed_data(str(features_path))
    
    # Get labeling config
    labeling_config = config.labeling_config
    barriers = labeling_config.get('barriers', {})
    
    # Apply triple barrier
    df_labeled = apply_triple_barrier(
        df,
        tp_multiplier=barriers.get('tp_multiplier', 2.0),
        sl_multiplier=barriers.get('sl_multiplier', 1.0),
        time_bars=barriers.get('time_bars', 12),
        atr_col='atr_14'
    )
    
    # Save
    output_path = Path(config.paths.data_labels) / "labeled_dataset.parquet"
    save_processed_data(df_labeled, str(output_path))
    
    logger.info("=" * 60)
    logger.info("✓ Labels built successfully")
    logger.info(f"Output: {output_path}")
    logger.info(f"Samples: {len(df_labeled)}")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
