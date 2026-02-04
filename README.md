# Full Marketing ETL Pipeline — Google Ads, GA4, Python & Power BI

This project is a full end-to-end **Marketing Analytics ETL Pipeline**.

It uses:

- **Python** (Pandas, NumPy, Scikit-learn, XGBoost, PuLP)
- **Google Ads** (simulated via Kaggle marketing dataset)
- **Google Analytics 4 (GA4)** sample ecommerce events
- **Power BI** for dashboards

The goal is to demonstrate how a modern marketing team can:

1. Collect data from Ads + Analytics sources  
2. Clean and unify the data  
3. Calculate core marketing KPIs  
4. Train ML models (ROAS & CPA prediction)  
5. Optimize marketing budget using Linear Programming  
6. Send final datasets to Power BI  

---

## 1. Project Structure

```
project_full_marketing_pipeline/
│
├── assets/                     # Images, diagrams for documentation
│   ├── marketing_etl_pipeline.png
│   ├── etl_pipeline_architecture.png
│   └── ...
│
├── data/
│   ├── raw/                    # Input CSVs (Ads + GA4) - PLACE DATA HERE
│   │   ├── Brand_Sales_AdSpend_Data.csv
│   │   └── ga4_obfuscated_sample_ecommerce.csv
│   │
│   └── processed/              # Final outputs for Power BI (Generated)
│       ├── marketing_ga4_merged_with_kpis.csv
│       ├── product_country_performance.csv
│       ├── what_if_budget_simulation.csv
│       └── lp_budget_recommendations.csv
│
├── notebooks/                  # Jupyter Notebooks for analysis and experiments
│
├── powerbi/                    # Power BI dashboard files
│   └── marketing_etl_dashboard.pbix
│
├── reports/                    # Exported analysis reports
│
├── src/                        # Python ETL pipeline source code
│   ├── ads_etl.py              # Google Ads data processing
│   ├── ga4_etl.py              # GA4 data processing
│   ├── merge_etl.py            # Data merging logic
│   ├── kpi_engine.py           # KPI calculation logic
│   └── main_etl.py             # Master pipeline entry point
│
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 2. Pipeline Flow – High Level Diagram

![Marketing ETL Pipeline](assets/marketing_etl_pipeline.png)

---

## 3. ETL Pipeline Architecture (Technical)

![ETL Pipeline Architecture](assets/etl_pipeline_architecture.png)

---

## 4. Features Included

### Data Cleaning & Normalization
- Handles missing values  
- Standardizes naming conventions  
- Merges Ads + GA4 datasets  

### KPI Engine
Automatically calculates:
- ROAS (Return on Ad Spend)
- ROI (Return on Investment)
- CPA (Cost Per Acquisition)
- CTR (Click-Through Rate)
- Conversion Rate
- Profit
- Country & Product level performance

### Machine Learning Models
- Predict future ROAS  
- Predict CPA  
- Scikit-learn + XGBoost  

### Budget Optimization
Linear Programming model using **PuLP**:
- Allocates budget across channels  
- Maximizes revenue or conversions  

### Final Output
Delivered as **Power BI dashboard** (.pbix)

---

## 5. How to Run the Project

### **1. Install required libraries**
Ensure you have Python installed. Then run:
```bash
pip install -r requirements.txt
```

### **2. Prepare Data**
Place your raw data files in the `data/raw/` directory:
- `Brand_Sales_AdSpend_Data.csv`
- `ga4_obfuscated_sample_ecommerce.csv`

### **3. Run the full ETL pipeline**
Execute the main script from the `src` directory:
```bash
cd src
python main_etl.py
```

### **4. Outputs will be generated here:**
The processed files will be saved to:
```
data/processed/
```

Main output file for Power BI:
```
data/processed/processed_full_marketing_dataset.csv
```

---

## 6. Power BI Dashboard

After running the pipeline, open the dashboard file:
```
powerbi/marketing_etl_dashboard.pbix
```

Refresh the data source in Power BI to point to the new `data/processed/processed_full_marketing_dataset.csv` file if necessary.

