"""
Unit tests for KPI Engine module.

Tests the calculate_kpis function with various edge cases
including division by zero, missing columns, and data validation.
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from kpi_engine import calculate_kpis


class TestCalculateKPIs:
    """Test suite for calculate_kpis function."""

    def test_profit_calculation(self):
        """Test that Profit = Total Sales - Total Ad Spend."""
        df = pd.DataFrame({
            "Total Sales": [1000, 2000, 500],
            "Total Ad Spend": [200, 400, 100],
            "Order Count": [10, 20, 5]
        })
        result = calculate_kpis(df)
        
        expected_profit = [800, 1600, 400]
        assert result["Profit"].tolist() == expected_profit

    def test_roas_calculation(self):
        """Test ROAS = Total Sales / Total Ad Spend."""
        df = pd.DataFrame({
            "Total Sales": [1000, 2000],
            "Total Ad Spend": [200, 500],
            "Order Count": [10, 20]
        })
        result = calculate_kpis(df)
        
        # ROAS: 1000/200 = 5.0, 2000/500 = 4.0
        assert result["ROAS"].tolist() == [5.0, 4.0]

    def test_roas_zero_spend(self):
        """Test ROAS handles zero ad spend (division by zero)."""
        df = pd.DataFrame({
            "Total Sales": [1000],
            "Total Ad Spend": [0],
            "Order Count": [10]
        })
        result = calculate_kpis(df)
        
        # Should return 0 (filled NaN) when ad spend is 0
        assert result["ROAS"].iloc[0] == 0

    def test_cpa_calculation(self):
        """Test CPA = Total Ad Spend / Order Count."""
        df = pd.DataFrame({
            "Total Sales": [1000],
            "Total Ad Spend": [200],
            "Order Count": [10]
        })
        result = calculate_kpis(df)
        
        # CPA: 200 / 10 = 20.0
        assert result["CPA"].iloc[0] == 20.0

    def test_cpa_zero_orders(self):
        """Test CPA handles zero orders (division by zero)."""
        df = pd.DataFrame({
            "Total Sales": [1000],
            "Total Ad Spend": [200],
            "Order Count": [0]
        })
        result = calculate_kpis(df)
        
        # Should return 0 (filled NaN) when orders is 0
        assert result["CPA"].iloc[0] == 0

    def test_ctr_calculation(self):
        """Test CTR = Clicks / Impressions."""
        df = pd.DataFrame({
            "Total Sales": [1000],
            "Total Ad Spend": [200],
            "Order Count": [10],
            "Clicks": [100],
            "Impressions": [1000]
        })
        result = calculate_kpis(df)
        
        # CTR: 100 / 1000 = 0.1
        assert result["CTR"].iloc[0] == 0.1

    def test_ctr_missing_columns(self):
        """Test CTR defaults to 0 when Clicks/Impressions columns missing."""
        df = pd.DataFrame({
            "Total Sales": [1000],
            "Total Ad Spend": [200],
            "Order Count": [10]
        })
        result = calculate_kpis(df)
        
        assert result["CTR"].iloc[0] == 0.0

    def test_cpc_calculation(self):
        """Test CPC = Total Ad Spend / Clicks."""
        df = pd.DataFrame({
            "Total Sales": [1000],
            "Total Ad Spend": [200],
            "Order Count": [10],
            "Clicks": [50]
        })
        result = calculate_kpis(df)
        
        # CPC: 200 / 50 = 4.0
        assert result["CPC"].iloc[0] == 4.0

    def test_conversion_rate_calculation(self):
        """Test ConvRate = Transactions / Clicks."""
        df = pd.DataFrame({
            "Total Sales": [1000],
            "Total Ad Spend": [200],
            "Order Count": [10],
            "Clicks": [100],
            "Transactions": [5]
        })
        result = calculate_kpis(df)
        
        # ConvRate: 5 / 100 = 0.05
        assert result["ConvRate"].iloc[0] == 0.05

    def test_all_kpi_columns_present(self):
        """Test that all expected KPI columns are added."""
        df = pd.DataFrame({
            "Total Sales": [1000],
            "Total Ad Spend": [200],
            "Order Count": [10]
        })
        result = calculate_kpis(df)
        
        expected_cols = ["ROAS", "CPA", "CTR", "CPC", "ConvRate", "Profit"]
        for col in expected_cols:
            assert col in result.columns, f"Missing column: {col}"

    def test_validity_flags(self):
        """Test that validity flags are added."""
        df = pd.DataFrame({
            "Total Sales": [1000, 500],
            "Total Ad Spend": [200, 0],
            "Order Count": [10, 0]
        })
        result = calculate_kpis(df)
        
        assert "Valid_ROAS" in result.columns
        assert "Valid_CPA" in result.columns

    def test_missing_values_filled(self):
        """Test that NaN and missing values are handled."""
        df = pd.DataFrame({
            "Total Sales": [1000, None],
            "Total Ad Spend": [None, 200],
            "Order Count": [10, 20]
        })
        result = calculate_kpis(df)
        
        # Check no NaN in KPI columns
        kpi_cols = ["ROAS", "CPA", "CTR", "CPC", "ConvRate", "Profit"]
        for col in kpi_cols:
            assert not result[col].isna().any(), f"NaN found in {col}"


class TestKPIEdgeCases:
    """Edge case tests for KPI calculations."""

    def test_empty_dataframe(self):
        """Test handling of empty DataFrame."""
        df = pd.DataFrame({
            "Total Sales": [],
            "Total Ad Spend": [],
            "Order Count": []
        })
        result = calculate_kpis(df)
        assert len(result) == 0

    def test_large_values(self):
        """Test handling of large numeric values."""
        df = pd.DataFrame({
            "Total Sales": [1e12],
            "Total Ad Spend": [1e9],
            "Order Count": [1000000]
        })
        result = calculate_kpis(df)
        
        # ROAS: 1e12 / 1e9 = 1000
        assert result["ROAS"].iloc[0] == 1000.0

    def test_negative_values(self):
        """Test handling of negative values (refunds, etc.)."""
        df = pd.DataFrame({
            "Total Sales": [-100],
            "Total Ad Spend": [50],
            "Order Count": [2]
        })
        result = calculate_kpis(df)
        
        # Profit: -100 - 50 = -150
        assert result["Profit"].iloc[0] == -150


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
