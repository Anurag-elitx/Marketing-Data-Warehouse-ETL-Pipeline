import os
import pandas as pd


def load_ads_data(data_dir: str,
                  filename: str = "Brand_Sales_AdSpend_Data.csv") -> pd.DataFrame:
    """
    Load and clean marketing (ads) data.

    Parameters
    ----------
    data_dir : str
        Root data folder (e.g. ../data).
    filename : str
        CSV file name for the ads dataset.

    Returns
    -------
    ads : pd.DataFrame
    """
    ads_file_path = os.path.join(data_dir, filename)

    if not os.path.exists(ads_file_path):
        raise FileNotFoundError(
            f"Ads data file not found: {ads_file_path}. "
            f"Please place the file in the 'data' folder."
        )

    ads = pd.read_csv(ads_file_path)

    # Clean column names (remove hidden spaces, non-breaking spaces, etc.)
    ads.columns = ads.columns.str.replace(u"\xa0", "", regex=True)
    ads.columns = ads.columns.str.strip()

    # Ensure Date is datetime
    if "Date" in ads.columns:
        ads["Date"] = pd.to_datetime(ads["Date"])

    print("Ads data shape:", ads.shape)
    print("Ads columns after cleaning:")
    print(ads.columns.tolist())
    print(ads.head())

    return ads
