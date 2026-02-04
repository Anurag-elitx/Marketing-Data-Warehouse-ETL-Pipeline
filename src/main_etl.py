import os
from ads_etl import load_ads_data
from ga4_etl import load_ga4_data
from merge_etl import merge_ads_ga4
from kpi_engine import calculate_kpis

def main():

    # PROJECT ROOT
    project_root = os.path.dirname(os.path.abspath(__file__))
    # data_dir now points to the project root's data folder
    data_dir = os.path.join(project_root, "..", "data")
    raw_dir = os.path.join(data_dir, "raw")
    processed_dir = os.path.join(data_dir, "processed")

    print(" Starting Full Marketing Pipeline...")

    # 1) Load Ads Data
    print("\n Loading Ads Data...")
    ads_df = load_ads_data(raw_dir)

    # 2) Load GA4 Data
    print("\n Loading GA4 Data...")
    ga4_df = load_ga4_data(raw_dir)

    # 3) Merge Ads + GA4
    print("\n Merging Ads + GA4 Data...")
    merged_df = merge_ads_ga4(ads_df, ga4_df)

    # 4) Calculate KPIs
    print("\n Calculating KPIs...")
    final_df = calculate_kpis(merged_df)

    # 5) Save Final Output
    output_path = os.path.join(processed_dir, "processed_full_marketing_dataset.csv")
    final_df.to_csv(output_path, index=False)

    print("\n Pipeline completed successfully!")
    print(f"Final dataset saved to: {output_path}")


if __name__ == "__main__":
    main()
