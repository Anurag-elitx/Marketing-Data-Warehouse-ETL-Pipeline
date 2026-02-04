import pandas as pd
import numpy as np


def calculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate marketing KPIs such as ROAS, CPA, CTR, CPC, Conversion Rate, and Profit.

    Parameters
    ----------
    df : pd.DataFrame
        Merged dataset containing Ads + GA4 metrics.

    Returns
    -------
    pd.DataFrame
        Updated DataFrame with new KPI columns.
    """

    # Profit
    df["Profit"] = df["Total Sales"].fillna(0) - df["Total Ad Spend"].fillna(0)

    # ROAS = Total Sales / Total Ad Spend
    df["ROAS"] = np.where(
        df["Total Ad Spend"] > 0,
        df["Total Sales"] / df["Total Ad Spend"],
        np.nan,
    )

    # CPA = Total Ad Spend / Order Count
    df["CPA"] = np.where(
        df["Order Count"] > 0,
        df["Total Ad Spend"] / df["Order Count"],
        np.nan,
    )

    # CTR = Clicks / Impressions
    if "Clicks" in df.columns and "Impressions" in df.columns:
        df["CTR"] = df["Clicks"] / df["Impressions"].replace(0, np.nan)
        df["CTR"] = df["CTR"].replace([np.inf, -np.inf], np.nan).fillna(0)
    else:
        df["CTR"] = 0.0

    # CPC = Total Ad Spend / Clicks
    if "Clicks" in df.columns:
        df["CPC"] = df["Total Ad Spend"] / df["Clicks"].replace(0, np.nan)
        df["CPC"] = df["CPC"].replace([np.inf, -np.inf], np.nan).fillna(0)
    else:
        df["CPC"] = 0.0

    # Conversion Rate = Transactions / Clicks
    if "Transactions" in df.columns and "Clicks" in df.columns:
        df["ConvRate"] = df["Transactions"] / df["Clicks"].replace(0, np.nan)
        df["ConvRate"] = df["ConvRate"].replace([np.inf, -np.inf], np.nan).fillna(0)
    else:
        df["ConvRate"] = 0.0

    # Clean infinities and fill NaNs
    kpi_cols = ["ROAS", "CPA", "Profit", "CTR", "CPC", "ConvRate"]
    df[kpi_cols] = df[kpi_cols].replace([np.inf, -np.inf], np.nan).fillna(0)

    # KPI validity flags
    df["Valid_ROAS"] = df["ROAS"].notna()
    df["Valid_CPA"] = df["CPA"].notna()

    return df


if __name__ == "__main__":
    print("KPI Engine module loaded. Use calculate_kpis(df) inside your pipeline.")
