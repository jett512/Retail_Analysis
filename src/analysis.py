import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def metric_correlations(df, output_csv=None, output_fig=None):
    # Use metrics relevant to sales and profitability (excluding product_cost METRIC_1)
    metric_cols = [c for c in df.columns if c.startswith('METRIC_')]
    corr = df[metric_cols].corr()

    if output_csv:
        corr.to_csv(output_csv)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Correlation Matrix of Metrics')

    if output_fig:
        fig.savefig(output_fig)
    plt.close(fig)

    return corr, fig


def sales_and_margin_analysis(df_or_list, output_dir=None):
    if isinstance(df_or_list, pd.DataFrame):
        combined_df = df_or_list.copy()
    else:
        combined_df = pd.concat(df_or_list, ignore_index=True)

    # Use METRIC_3 for sales revenue and METRIC_2 for profit margin
    grouped_sales = combined_df.groupby(['ATTRIBUTE_2', 'ATTRIBUTE_3'])['METRIC_3'].mean().round(2).reset_index(name='avg_sales_revenue')
    grouped_margin = combined_df.groupby(['ATTRIBUTE_2', 'ATTRIBUTE_3'])['METRIC_2'].mean().round(2).reset_index(name='avg_profit_margin')

    combined = pd.merge(grouped_sales, grouped_margin, on=['ATTRIBUTE_2', 'ATTRIBUTE_3'])

    combined_perf = combined.copy()
    combined_perf['performance_score'] = combined_perf['avg_sales_revenue'] * combined_perf['avg_profit_margin']

    def top_bottom(df, col):
        return df.sort_values(col, ascending=False), df.sort_values(col)

    top_sales, bottom_sales = top_bottom(combined, 'avg_sales_revenue')
    top_margin, bottom_margin = top_bottom(combined, 'avg_profit_margin')
    top_perf, bottom_perf = top_bottom(round(combined_perf,2), 'performance_score')

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        top_sales.to_csv(output_dir / "top_sales_segments.csv", index=False)
        bottom_sales.to_csv(output_dir / "bottom_sales_segments.csv", index=False)
        top_margin.to_csv(output_dir / "top_margin_segments.csv", index=False)
        bottom_margin.to_csv(output_dir / "bottom_margin_segments.csv", index=False)
        top_perf.to_csv(output_dir / "top_performers.csv", index=False)
        bottom_perf.to_csv(output_dir / "bottom_performers.csv", index=False)

    return top_sales, bottom_sales, top_margin, bottom_margin, top_perf, bottom_perf

