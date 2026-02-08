import os
import pandas as pd


def load_ga4_country_summary(
    data_dir: str,
    filename: str = "ga4_obfuscated_sample_ecommerce.csv"
) -> pd.DataFrame:
    """
    Load raw GA4 events and aggregate to Date + Country level.

    Returns
    -------
    ga4_country : pd.DataFrame
        Columns: Date, Country, Sessions, Transactions, Revenue
    """
    ga4_file_path = os.path.join(data_dir, filename)

    if not os.path.exists(ga4_file_path):
        raise FileNotFoundError(
            f"GA4 data file not found: {ga4_file_path}. "
            f"Please place the file in the 'data' folder."
        )

    ga4 = pd.read_csv(ga4_file_path)

    print("GA4 data shape:", ga4.shape)
    print("GA4 columns:")
    print(ga4.columns)

    # 1) event_timestamp → Date
    ga4["event_timestamp"] = pd.to_datetime(
        ga4["event_timestamp"], unit="us", errors="coerce"
    )
    ga4["Date"] = pd.to_datetime(ga4["event_timestamp"].dt.date)

    # 2) geography
    ga4["Country"] = ga4.get("geo.country")
    ga4["City"] = ga4.get("geo.city")

    # 3) user_id for sessions
    ga4["user_id"] = ga4.get("user_pseudo_id")

    # 4) Sessions (unique users per Date / Country / City)
    sessions_df = (
        ga4.groupby(["Date", "Country", "City"])["user_id"]
        .nunique()
        .reset_index()
        .rename(columns={"user_id": "Sessions"})
    )

    # 5) Purchase flag
    ga4["is_purchase"] = (ga4["event_name"] == "purchase").astype(int)

    # 6) Revenue
    if "event_params.value.double_value" in ga4.columns:
        ga4["Revenue"] = ga4["event_params.value.double_value"].fillna(0)
    else:
        ga4["Revenue"] = 0

    # 7) Transactions & Revenue
    transactions_df = (
        ga4.groupby(["Date", "Country", "City"])
        .agg(
            Transactions=("is_purchase", "sum"),
            Revenue=("Revenue", "sum"),
        )
        .reset_index()
    )

    # 8) Merge Sessions + Transactions + Revenue
    ga4_summary = sessions_df.merge(
        transactions_df,
        on=["Date", "Country", "City"],
        how="left",
    )

    ga4_summary["Transactions"] = ga4_summary["Transactions"].fillna(0)
    ga4_summary["Revenue"] = ga4_summary["Revenue"].fillna(0)

    # 9) Aggregate to Date + Country
    ga4_country = (
        ga4_summary.groupby(["Date", "Country"], as_index=False)[
            ["Sessions", "Transactions", "Revenue"]
        ].sum()
    )

    print("GA4 country-level summary shape:", ga4_country.shape)
    print(ga4_country.head())

    return ga4_country


def load_ga4_data(data_dir: str, filename: str = "ga4_obfuscated_sample_ecommerce.csv") -> pd.DataFrame:
    """
    Load and process GA4 ecommerce data.
    
    This is an alias for load_ga4_country_summary() for backward compatibility.
    
    Parameters
    ----------
    data_dir : str
        Path to directory containing the GA4 data file.
    filename : str
        Name of the GA4 CSV file (default: ga4_obfuscated_sample_ecommerce.csv)
    
    Returns
    -------
    pd.DataFrame
        Aggregated GA4 data by Date and Country with Sessions, Transactions, Revenue.
    """
    return load_ga4_country_summary(data_dir, filename)

