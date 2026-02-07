"""
Pipeline: Build clean dataset from raw CSV
"""
import sys
from pathlib import Path
from loguru import logger

from aurum_edge.core.config import Config
from aurum_edge.core.logging import setup_logging
from aurum_edge.data.ingest import load_mt5_csv, save_processed_data
from aurum_edge.data.validate import run_full_validation
from aurum_edge.data.transform import clean_data

def main(mode='build'):
    """Main pipeline"""
    # Setup
    config = Config.from_yaml()
    setup_logging(log_dir=config.paths.logs)
    
    logger.info("=" * 60)
    logger.info("PIPELINE: Build Dataset")
    logger.info("=" * 60)
    
    # Find CSV file
    raw_dir = Path(config.paths.data_raw)
    csv_files = list(raw_dir.glob("*.csv"))
    
    if not csv_files:
        logger.error(f"No CSV files found in {raw_dir}")
        logger.error("Please export data from MT5 and place in data/raw/")
        sys.exit(1)
    
    csv_file = csv_files[0]
    logger.info(f"Loading CSV: {csv_file}")
    
    # Load data
    df = load_mt5_csv(str(csv_file))
    
    # Validate
    asset_config = config.asset_config
    data_quality_config = config.load_sub_config('data_quality') if hasattr(config, 'data_quality') else {}
    
    logger.info("Validating data quality...")
    validation_passed = run_full_validation(df, {
        'min_rows': 1000,
        'outlier_threshold': 5.0
    })
    
    if mode == 'validate':
        if validation_passed:
            logger.info("✓ Validation PASSED")
            sys.exit(0)
        else:
            logger.error("✗ Validation FAILED")
            sys.exit(1)
    
    if not validation_passed:
        logger.warning("Validation failed but continuing (mode=build)")
    
    # Clean
    df_clean = clean_data(df)
    
    # Save
    output_path = Path(config.paths.data_processed) / "dataset_clean.parquet"
    save_processed_data(df_clean, str(output_path))
    
    logger.info("=" * 60)
    logger.info("✓ Dataset build complete")
    logger.info(f"Output: {output_path}")
    logger.info(f"Rows: {len(df_clean)}")
    logger.info("=" * 60)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'build'
    main(mode)
