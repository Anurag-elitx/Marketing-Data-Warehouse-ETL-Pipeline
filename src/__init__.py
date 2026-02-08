"""
Marketing ETL Pipeline - Source Package.

This package contains the core ETL modules for processing
marketing data from Google Ads and GA4 analytics.

Modules:
    ads_etl: Google Ads data loading and cleaning
    ga4_etl: GA4 analytics data processing
    merge_etl: Data merging logic
    kpi_engine: Marketing KPI calculations
    config: Centralized configuration
    logger: Logging setup
"""

from .config import (
    PROJECT_ROOT,
    DATA_DIR,
    RAW_DIR,
    PROCESSED_DIR,
    ensure_directories_exist
)
from .logger import setup_logger, logger

__version__ = "1.1.0"
__author__ = "Anurag"

__all__ = [
    "PROJECT_ROOT",
    "DATA_DIR", 
    "RAW_DIR",
    "PROCESSED_DIR",
    "ensure_directories_exist",
    "setup_logger",
    "logger"
]
