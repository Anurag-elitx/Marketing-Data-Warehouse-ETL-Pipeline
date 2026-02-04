import pandas as pd

def merge_ads_ga4(ads_df: pd.DataFrame,
                  ga4_df: pd.DataFrame,
                  on_cols=["Date", "Country"]) -> pd.DataFrame:
    """
    Merge Ads data + GA4 aggregated data by Date & Country.

    Parameters
    ----------
    ads_df : pd.DataFrame
        Cleaned marketing (ads) dataset.
    ga4_df : pd.DataFrame
        GA4 aggregated (country-level) dataset.
    on_cols : list
        Keys to merge on (default: ["Date", "Country"])

    Returns
    -------
    pd.DataFrame
        Combined dataset with ads + GA4 metrics merged.
    """

    # Ensure datetime consistency
    if "Date" in ads_df.columns:
        ads_df["Date"] = pd.to_datetime(ads_df["Date"])
    if "Date" in ga4_df.columns:
        ga4_df["Date"] = pd.to_datetime(ga4_df["Date"])

    # Merge
    merged = pd.merge(
        ads_df,
        ga4_df,
        on=on_cols,
        how="left"
    )

    # Fill GA4 missing values (sessions, transactions, revenue)
    for col in ["Sessions", "Transactions", "Revenue"]:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0)

    # Clean column names for safety
    merged.columns = merged.columns.str.replace("\xa0", "", regex=True)
    merged.columns = merged.columns.str.strip()

    return merged
