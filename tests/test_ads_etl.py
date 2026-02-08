"""
Unit tests for Ads ETL module.

Tests the load_ads_data function with various scenarios
including file handling, data cleaning, and date parsing.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os
import tempfile

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from ads_etl import load_ads_data


class TestLoadAdsData:
    """Test suite for load_ads_data function."""

    def test_file_not_found(self):
        """Test that FileNotFoundError is raised for missing file."""
        with pytest.raises(FileNotFoundError):
            load_ads_data("/nonexistent/path")

    def test_loads_csv_successfully(self, tmp_path):
        """Test successful CSV loading."""
        # Create test CSV
        test_data = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-02"],
            "Country": ["US", "UK"],
            "Total Ad Spend": [100, 200]
        })
        csv_path = tmp_path / "Brand_Sales_AdSpend_Data.csv"
        test_data.to_csv(csv_path, index=False)
        
        result = load_ads_data(str(tmp_path))
        
        assert len(result) == 2
        assert "Date" in result.columns
        assert "Country" in result.columns

    def test_date_conversion(self, tmp_path):
        """Test that Date column is converted to datetime."""
        test_data = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-02"],
            "Country": ["US", "UK"]
        })
        csv_path = tmp_path / "Brand_Sales_AdSpend_Data.csv"
        test_data.to_csv(csv_path, index=False)
        
        result = load_ads_data(str(tmp_path))
        
        assert pd.api.types.is_datetime64_any_dtype(result["Date"])

    def test_column_name_cleaning(self, tmp_path):
        """Test that column names are cleaned."""
        test_data = pd.DataFrame({
            "Date ": ["2024-01-01"],  # Trailing space
            " Country": ["US"],  # Leading space
            "Total\xa0Spend": [100]  # Non-breaking space
        })
        csv_path = tmp_path / "Brand_Sales_AdSpend_Data.csv"
        test_data.to_csv(csv_path, index=False)
        
        result = load_ads_data(str(tmp_path))
        
        # Check columns are stripped
        assert "Date" in result.columns or "Date " not in result.columns
        assert "Country" in result.columns or " Country" not in result.columns

    def test_custom_filename(self, tmp_path):
        """Test loading with custom filename."""
        test_data = pd.DataFrame({
            "Date": ["2024-01-01"],
            "Country": ["US"]
        })
        csv_path = tmp_path / "custom_ads_data.csv"
        test_data.to_csv(csv_path, index=False)
        
        result = load_ads_data(str(tmp_path), filename="custom_ads_data.csv")
        
        assert len(result) == 1


class TestAdsDataCleaning:
    """Test data cleaning in ads_etl."""

    def test_handles_missing_date_column(self, tmp_path):
        """Test handling when Date column is missing."""
        test_data = pd.DataFrame({
            "Country": ["US"],
            "Total Ad Spend": [100]
        })
        csv_path = tmp_path / "Brand_Sales_AdSpend_Data.csv"
        test_data.to_csv(csv_path, index=False)
        
        result = load_ads_data(str(tmp_path))
        
        # Should not fail, Date column just won't be converted
        assert len(result) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
