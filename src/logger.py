"""
Centralized logging configuration for Marketing ETL Pipeline.

This module provides a standardized logging setup with both console
and file handlers for consistent logging across all ETL modules.
"""

import logging
import os
from datetime import datetime


def setup_logger(
    name: str = "marketing_etl",
    log_level: int = logging.INFO,
    log_dir: str = None
) -> logging.Logger:
    """
    Configure and return a logger with console and file handlers.

    Parameters
    ----------
    name : str
        Logger name (default: "marketing_etl")
    log_level : int
        Logging level (default: logging.INFO)
    log_dir : str, optional
        Directory for log files. If None, logs to ../logs/

    Returns
    -------
    logging.Logger
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    logger.setLevel(log_level)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler
    if log_dir is None:
        log_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            "logs"
        )
    
    os.makedirs(log_dir, exist_ok=True)
    
    log_filename = f"etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    logger.info(f"Logger initialized. Log file: {log_path}")
    
    return logger


# Create default logger instance
logger = setup_logger()


if __name__ == "__main__":
    # Test the logger
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    print("Logger test complete. Check the logs/ directory.")
