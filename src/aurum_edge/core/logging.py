"""
Structured logging setup using loguru
"""
import sys
from pathlib import Path
from typing import Optional

from loguru import logger


def setup_logging(
    log_dir: str = "logs",
    log_level: str = "INFO",
    rotation: str = "100 MB",
    retention: str = "30 days",
    log_file: Optional[str] = None,
) -> None:
    """
    Configure logging for the application
    
    Args:
        log_dir: Directory for log files
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR)
        rotation: When to rotate log files
        retention: How long to keep log files
        log_file: Optional specific log file name
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )
    
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Add file handler
    if log_file is None:
        log_file = log_path / "aurum_edge_{time:YYYY-MM-DD}.log"
    else:
        log_file = log_path / log_file
    
    logger.add(
        str(log_file),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
        rotation=rotation,
        retention=retention,
        compression="zip",
        enqueue=True,  # Thread-safe
    )
    
    logger.info(f"Logging initialized - Level: {log_level}, File: {log_file}")


def get_logger(name: str):
    """
    Get a logger instance for a module
    
    Args:
        name: Module name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logger.bind(name=name)
