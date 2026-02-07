"""
Pipeline: Run paper trading
"""
import sys
from pathlib import Path
from loguru import logger

from aurum_edge.core.config import Config
from aurum_edge.core.logging import setup_logging
from aurum_edge.execution.paper import PaperTradingEngine
from aurum_edge.execution.human_approval import HumanApprovalSystem

def main():
    """Main pipeline"""
    # Setup
    config = Config.from_yaml()
    setup_logging(log_dir=config.paths.logs)
    
    logger.info("=" * 60)
    logger.info("PIPELINE: Paper Trading")
    logger.info("=" * 60)
    
    # Initialize systems
    paper_engine = PaperTradingEngine(initial_balance=1000.0)
    approval_system = HumanApprovalSystem(config.execution_config)
    
    # Demo signal
    signal_info = {
        'symbol': 'NAS100',
        'direction': 'long',
        'entry_price': 16500.0,
        'stop_loss': 16480.0,
        'take_profit': 16540.0,
        'position_size': 0.01,
        'confidence': 0.75
    }
    
    # Request approval
    approved = approval_system.request_approval(signal_info)
    
    if approved:
        logger.info("Trade approved - executing paper trade...")
        trade = paper_engine.execute_trade(
            entry_price=signal_info['entry_price'],
            direction=signal_info['direction'],
            size=signal_info['position_size'],
            stop_loss=signal_info['stop_loss'],
            take_profit=signal_info['take_profit']
        )
        
        # Simulate close
        paper_engine.close_trade(trade, exit_price=16530.0)
    
    # Summary
    summary = paper_engine.get_summary()
    logger.info("=" * 60)
    logger.info("Paper Trading Summary:")
    for key, value in summary.items():
        logger.info(f"  {key}: {value}")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
