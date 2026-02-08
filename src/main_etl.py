"""
Master ETL Pipeline Entry Point.

This module orchestrates the full marketing analytics pipeline:
1. Load Google Ads data
2. Load GA4 analytics data
3. Merge datasets
4. Calculate KPIs
5. Save processed output

Usage:
    python main_etl.py
"""

import os
import sys
import time
from datetime import datetime

# Add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ads_etl import load_ads_data
from ga4_etl import load_ga4_data
from merge_etl import merge_ads_ga4
from kpi_engine import calculate_kpis
from logger import setup_logger
from config import RAW_DIR, PROCESSED_DIR, OUTPUT_FILENAME, ensure_directories_exist


def main():
    """
    Execute the full marketing ETL pipeline.
    
    Raises
    ------
    FileNotFoundError
        If required input data files are missing.
    Exception
        For any unexpected errors during pipeline execution.
    """
    # Initialize logger
    logger = setup_logger("marketing_etl_main")
    
    # Ensure all directories exist
    ensure_directories_exist()
    
    pipeline_start = time.time()
    logger.info("=" * 60)
    logger.info("Starting Full Marketing ETL Pipeline")
    logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    try:
        # Step 1: Load Ads Data
        step_start = time.time()
        logger.info("[Step 1/5] Loading Google Ads data...")
        ads_df = load_ads_data(RAW_DIR)
        logger.info(f"Ads data loaded: {len(ads_df)} rows in {time.time() - step_start:.2f}s")

        # Step 2: Load GA4 Data
        step_start = time.time()
        logger.info("[Step 2/5] Loading GA4 analytics data...")
        ga4_df = load_ga4_data(RAW_DIR)
        logger.info(f"GA4 data loaded: {len(ga4_df)} rows in {time.time() - step_start:.2f}s")

        # Step 3: Merge Ads + GA4
        step_start = time.time()
        logger.info("[Step 3/5] Merging Ads and GA4 datasets...")
        merged_df = merge_ads_ga4(ads_df, ga4_df)
        logger.info(f"Merged data: {len(merged_df)} rows in {time.time() - step_start:.2f}s")

        # Step 4: Calculate KPIs
        step_start = time.time()
        logger.info("[Step 4/5] Calculating marketing KPIs...")
        final_df = calculate_kpis(merged_df)
        logger.info(f"KPIs calculated: {len(final_df.columns)} columns in {time.time() - step_start:.2f}s")

        # Step 5: Save Final Output
        step_start = time.time()
        logger.info("[Step 5/5] Saving processed dataset...")
        output_path = os.path.join(PROCESSED_DIR, OUTPUT_FILENAME)
        final_df.to_csv(output_path, index=False)
        logger.info(f"Output saved to: {output_path}")

        # Pipeline complete
        total_time = time.time() - pipeline_start
        logger.info("=" * 60)
        logger.info("Pipeline completed successfully!")
        logger.info(f"Total execution time: {total_time:.2f} seconds")
        logger.info(f"Output file: {output_path}")
        logger.info(f"Total rows processed: {len(final_df)}")
        logger.info("=" * 60)
        
        return final_df

    except FileNotFoundError as e:
        logger.error(f"Data file not found: {e}")
        logger.error("Please ensure the required CSV files are in the data/raw/ directory.")
        raise

    except Exception as e:
        logger.error(f"Pipeline failed with error: {type(e).__name__}: {e}")
        logger.exception("Full traceback:")
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nPipeline failed: {e}")
        sys.exit(1)
