"""
Unit tests for Merge ETL module.

Tests the merge_ads_ga4 function with various scenarios
including date handling, missing columns, and data validation.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from merge_etl import merge_ads_ga4


class TestMergeAdsGA4:
    """Test suite for merge_ads_ga4 function."""

    def test_basic_merge(self):
        """Test basic merge on Date and Country."""
        ads_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "Country": ["US", "UK"],
            "Total Ad Spend": [100, 200]
        })
        ga4_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "Country": ["US", "UK"],
            "Sessions": [1000, 2000],
            "Transactions": [50, 100],
            "Revenue": [5000, 10000]
        })
        
        result = merge_ads_ga4(ads_df, ga4_df)
        
        assert len(result) == 2
        assert "Sessions" in result.columns
        assert "Total Ad Spend" in result.columns

    def test_left_join_preserves_ads_data(self):
        """Test that left join preserves all ads data."""
        ads_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]),
            "Country": ["US", "UK", "DE"],
            "Total Ad Spend": [100, 200, 300]
        })
        ga4_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01"]),
            "Country": ["US"],
            "Sessions": [1000]
        })
        
        result = merge_ads_ga4(ads_df, ga4_df)
        
        # All 3 ads rows should be present
        assert len(result) == 3

    def test_missing_ga4_filled_with_zero(self):
        """Test that missing GA4 values are filled with 0."""
        ads_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01"]),
            "Country": ["US"],
            "Total Ad Spend": [100]
        })
        ga4_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-02"]),  # Different date
            "Country": ["UK"],  # Different country
            "Sessions": [1000],
            "Transactions": [50],
            "Revenue": [5000]
        })
        
        result = merge_ads_ga4(ads_df, ga4_df)
        
        # GA4 metrics should be 0 for the US row
        assert result["Sessions"].iloc[0] == 0
        assert result["Transactions"].iloc[0] == 0
        assert result["Revenue"].iloc[0] == 0

    def test_date_string_conversion(self):
        """Test that string dates are converted to datetime."""
        ads_df = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-02"],
            "Country": ["US", "UK"],
            "Total Ad Spend": [100, 200]
        })
        ga4_df = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-02"],
            "Country": ["US", "UK"],
            "Sessions": [1000, 2000]
        })
        
        result = merge_ads_ga4(ads_df, ga4_df)
        
        assert pd.api.types.is_datetime64_any_dtype(result["Date"])

    def test_column_name_cleaning(self):
        """Test that column names are cleaned (no weird spaces)."""
        ads_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01"]),
            "Country": ["US"],
            "Total\xa0Spend": [100]  # Non-breaking space
        })
        ga4_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01"]),
            "Country": ["US"],
            "Sessions": [1000]
        })
        
        result = merge_ads_ga4(ads_df, ga4_df)
        
        # Column should be cleaned
        assert "Total\xa0Spend" not in result.columns or "TotalSpend" in result.columns

    def test_custom_merge_keys(self):
        """Test merge with custom keys."""
        ads_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01"]),
            "Country": ["US"],
            "City": ["New York"],
            "Total Ad Spend": [100]
        })
        ga4_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01"]),
            "Country": ["US"],
            "City": ["New York"],
            "Sessions": [1000]
        })
        
        result = merge_ads_ga4(ads_df, ga4_df, on_cols=["Date", "Country", "City"])
        
        assert len(result) == 1
        assert result["Sessions"].iloc[0] == 1000

    def test_empty_dataframes(self):
        """Test handling of empty DataFrames."""
        ads_df = pd.DataFrame({
            "Date": pd.Series([], dtype="datetime64[ns]"),
            "Country": pd.Series([], dtype=str),
            "Total Ad Spend": pd.Series([], dtype=float)
        })
        ga4_df = pd.DataFrame({
            "Date": pd.Series([], dtype="datetime64[ns]"),
            "Country": pd.Series([], dtype=str),
            "Sessions": pd.Series([], dtype=int)
        })
        
        result = merge_ads_ga4(ads_df, ga4_df)
        
        assert len(result) == 0

    def test_duplicate_handling(self):
        """Test that duplicates in source data are handled."""
        ads_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
            "Country": ["US", "US"],
            "Total Ad Spend": [100, 150]  # Two rows for same date/country
        })
        ga4_df = pd.DataFrame({
            "Date": pd.to_datetime(["2024-01-01"]),
            "Country": ["US"],
            "Sessions": [1000]
        })
        
        result = merge_ads_ga4(ads_df, ga4_df)
        
        # Both ads rows should have the same session count
        assert len(result) == 2
        assert all(result["Sessions"] == 1000)


class TestMergeEdgeCases:
    """Edge case tests for merge function."""

    def test_missing_date_column(self):
        """Test behavior when Date column is missing."""
        ads_df = pd.DataFrame({
            "Country": ["US"],
            "Total Ad Spend": [100]
        })
        ga4_df = pd.DataFrame({
            "Country": ["US"],
            "Sessions": [1000]
        })
        
        # Should still work if merging only on Country
        result = merge_ads_ga4(ads_df, ga4_df, on_cols=["Country"])
        assert len(result) == 1

    def test_large_dataset_merge(self):
        """Test merge performance with larger dataset."""
        n_rows = 1000
        dates = pd.date_range("2024-01-01", periods=n_rows, freq="D")
        
        ads_df = pd.DataFrame({
            "Date": dates,
            "Country": ["US"] * n_rows,
            "Total Ad Spend": range(n_rows)
        })
        ga4_df = pd.DataFrame({
            "Date": dates,
            "Country": ["US"] * n_rows,
            "Sessions": range(n_rows)
        })
        
        result = merge_ads_ga4(ads_df, ga4_df)
        
        assert len(result) == n_rows


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
