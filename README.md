# Retail_Analysis
```
/Retail_Analysis/
│
├── Data/
│   ├── cleaned_dataset.csv
|   └── Dataset for Technical Interview 1.xlsx
├── Results/
│   ├── eda/
│   └── analysis/
├── src/
│   ├── preprocessing.py
│   └── eda.py
│   └── analysis.py
├── Notebooks/
│   ├── Quickstart.ipynb
│   └── Workflow.ipynb
|
├── config.yaml
└── main.py
└── requirements.txt
└── data_dictionary.csv
```

## Approach

- **Data Cleaning:**  
  Loaded raw Excel data, handled missing or malformed values, converted currency and percentage strings to numeric formats, and saved a cleaned CSV for downstream use.

- **Exploratory Data Analysis (EDA):**  
  Generated summary statistics, identified missing data, checked for duplicates, and detected outliers in both numeric and categorical data.  
  Used custom functions to analyze metrics despite ambiguous column names.

- **Analysis & Visualization:**  
  Calculated correlations between key metrics and created heatmaps for visual insight.  
  Performed segment-level sales and profit margin analyses grouped by categorical attributes to uncover performance patterns.

- **Presentation Preparation:**  
  Documented all steps, challenges, and insights in notebooks and scripts.  
  Visualized results with clear charts and tables to support narrative storytelling during the interview presentation.

## Challenges

- No data dictionary or clear variable definitions required assumption-making and iterative validation of metric meanings.  
- Ambiguous column names demanded flexible and modular code design to adapt analyses.  
- Handling mixed data formats (e.g., currency, percentages as strings) required robust cleaning routines.

## Key Findings

- Identified key metric correlations indicating potential relationships worth further investigation.  
- Detected segments with notably high or low sales and profit margins, providing actionable business insights.  
- Highlighted data quality issues such as missing values and outliers that could impact decision-making.

---

This project showcases a thoughtful and reproducible approach to working with ambiguous real-world data, emphasizing transparency, modular code, and effective communication of results.

```python
# Unzip the project archive
!unzip .../Retail_Analysis.zip

# Install required packages
!pip install -r .../Retail_Analysis/requirements.txt

import os
import pandas as pd

# Change working directory to the project folder
os.chdir('/content/Retail_Analysis')
print(f"Current working directory: {os.getcwd()}")

# Run the main pipeline
!python main.py

# Load the analysis result CSVs
df_1 = pd.read_csv('.../Results/analysis/top_margin_segments.csv')
df_2 = pd.read_csv('/content/Michaels/Results/analysis/bottom_margin_segments.csv')

df_3 = pd.read_csv('.../Results/analysis/top_sales_segments.csv')
df_4 = pd.read_csv('.../Results/analysis/bottom_sales_segments.csv')

# Print the dataframes to review the output
print("Top Margin Segments:")
print(df_1)
print("\nBottom Margin Segments:")
print(df_2)
print("\nTop Sales Segments:")
print(df_3)
print("\nBottom Sales Segments:")
print(df_4)
