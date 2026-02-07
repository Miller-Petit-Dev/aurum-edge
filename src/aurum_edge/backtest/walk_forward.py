"""Walk-forward validation"""
from loguru import logger
from aurum_edge.data.split import get_walk_forward_splits

def run_walk_forward(df, model_fn, config):
    """
    Run walk-forward validation
    
    Args:
        df: Full dataset
        model_fn: Function to train and predict
        config: Walk-forward configuration
    """
    logger.info("Starting walk-forward validation...")
    
    splits = get_walk_forward_splits(
        df,
        train_months=config['windows']['train_months'],
        test_weeks=config['windows']['test_weeks'],
        step_weeks=config['windows']['step_weeks']
    )
    
    all_metrics = []
    
    for i, (train_df, test_df) in enumerate(splits):
        logger.info(f"Fold {i+1}/{len(splits)}: Train {len(train_df)}, Test {len(test_df)}")
        
        metrics = model_fn(train_df, test_df)
        all_metrics.append(metrics)
    
    logger.info(f"Walk-forward complete: {len(all_metrics)} folds")
    return all_metrics
