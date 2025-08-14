import pandas as pd
from pathlib import Path
import yaml

from src.preprocessing import preprocess_dataset
from src.eda import analyze_dataset, metric_analysis, summary_statistics, detect_outliers
from src.analysis import metric_correlations, sales_and_margin_analysis

# Load paths from config.yaml
with open("config.yaml") as f:
    paths = yaml.safe_load(f)["paths"]

def main():
    # Preprocess dataset
    df = preprocess_dataset(paths["raw_data"], paths["processed_data"])

    # Ensure EDA results directory exists
    Path(paths["dataset_analysis"]).parent.mkdir(parents=True, exist_ok=True)

    # Run EDA functions and save outputs
    analyze_dataset(df).to_csv(paths["dataset_analysis"], index=False)
    metric_analysis(df).to_csv(paths["metric_analysis"], index=False)
    summary_statistics(df).to_csv(paths["summary_statistics"], index=False)
    detect_outliers(df).to_csv(paths["outliers"], index=False)

    # Ensure analysis results directory exists
    Path(paths["sales_margin_segments"]).parent.mkdir(parents=True, exist_ok=True)

    # Run analysis functions and save outputs
    metric_correlations(
        df,
        output_csv=paths["correlation_matrix"],
        output_fig=paths["correlation_plot"]
    )
    sales_and_margin_analysis(
        df,
        output_dir=Path(paths["sales_margin_segments"]).parent
    )

if __name__ == "__main__":
    main()
