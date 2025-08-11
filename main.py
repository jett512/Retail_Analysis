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
    # Preprocess
    df = preprocess_dataset(paths["raw_data"], paths["processed_data"])

    # Create EDA results folder
    eda_results_dir = Path(paths["eda_results"]).parent
    eda_results_dir.mkdir(parents=True, exist_ok=True)

    # Run EDA functions and save outputs
    analyze_dataset(df).to_csv(eda_results_dir / "dataset_analysis.csv", index=False)
    metric_analysis(df).to_csv(eda_results_dir / "metric_analysis.csv", index=False)
    summary_statistics(df).to_csv(eda_results_dir / "summary_statistics.csv", index=False)
    detect_outliers(df).to_csv(eda_results_dir / "outliers.csv", index=False)

    # Create Analysis results folder
    analysis_results_dir = Path(paths["analysis_results"]).parent
    analysis_results_dir.mkdir(parents=True, exist_ok=True)

    # Run analysis functions and save outputs
    metric_correlations(
        df,
        output_csv=analysis_results_dir / "correlation_matrix.csv",
        output_fig=Path(paths["correlation_plot"])
    )
    sales_and_margin_analysis(df, output_dir=analysis_results_dir)

if __name__ == "__main__":
    main()
