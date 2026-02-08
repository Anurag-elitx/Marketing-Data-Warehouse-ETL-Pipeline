"""
Configuration constants for Marketing ETL Pipeline.

This module centralizes all file paths, column names, and default values
used across the ETL pipeline for easier maintenance and consistency.
"""

import os

# Project structure paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")

# Input file names
ADS_FILENAME = "Brand_Sales_AdSpend_Data.csv"
GA4_FILENAME = "ga4_obfuscated_sample_ecommerce.csv"

# Output file names
OUTPUT_FILENAME = "processed_full_marketing_dataset.csv"
MERGED_KPI_FILENAME = "marketing_ga4_merged_with_kpis.csv"
PRODUCT_PERFORMANCE_FILENAME = "product_country_performance.csv"
BUDGET_SIMULATION_FILENAME = "what_if_budget_simulation.csv"
LP_RECOMMENDATIONS_FILENAME = "lp_budget_recommendations.csv"

# Column names used across modules
DATE_COL = "Date"
COUNTRY_COL = "Country"
CITY_COL = "City"

# Ads data columns
ADS_COLUMNS = {
    "spend": "Total Ad Spend",
    "sales": "Total Sales",
    "orders": "Order Count",
    "clicks": "Clicks",
    "impressions": "Impressions"
}

# GA4 data columns
GA4_COLUMNS = {
    "timestamp": "event_timestamp",
    "event_name": "event_name",
    "user_id": "user_pseudo_id",
    "country": "geo.country",
    "city": "geo.city",
    "revenue": "event_params.value.double_value"
}

# KPI column names
KPI_COLUMNS = [
    "ROAS",      # Return on Ad Spend
    "CPA",       # Cost Per Acquisition
    "CTR",       # Click-Through Rate
    "CPC",       # Cost Per Click
    "ConvRate",  # Conversion Rate
    "Profit"     # Profit margin
]

# Default merge keys
MERGE_KEYS = [DATE_COL, COUNTRY_COL]

# Numeric fill value for missing data
DEFAULT_FILL_VALUE = 0


def ensure_directories_exist():
    """Create required directories if they don't exist."""
    for directory in [RAW_DIR, PROCESSED_DIR, LOGS_DIR, REPORTS_DIR]:
        os.makedirs(directory, exist_ok=True)


if __name__ == "__main__":
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Raw Data: {RAW_DIR}")
    print(f"Processed Data: {PROCESSED_DIR}")
    ensure_directories_exist()
    print("All directories verified/created.")
