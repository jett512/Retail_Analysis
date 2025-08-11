import pandas as pd
from pathlib import Path


def metric_correlations(df, output_csv=None, output_fig=None):
    metric_cols = [c for c in df.columns if c.startswith('METRIC_')]
    corr = df[metric_cols].corr()

    if output_csv:
        corr.to_csv(output_csv)

    import matplotlib.pyplot as plt
    import seaborn as sns

    fig, ax = plt.subplots(figsize=(10,8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Correlation Matrix of Metrics')

    if output_fig:
        fig.savefig(output_fig)
    plt.close(fig)

    return corr


def sales_and_margin_analysis(df, output_dir=None):
    grouped_sales = df.groupby(['ATTRIBUTE_2', 'ATTRIBUTE_3'])['METRIC_1'].mean().round(2).reset_index(name='avg_sales_revenue')
    grouped_margin = df.groupby(['ATTRIBUTE_2', 'ATTRIBUTE_3'])['METRIC_2'].mean().round(2).reset_index(name='avg_profit_margin')

    combined = pd.merge(grouped_sales, grouped_margin, on=['ATTRIBUTE_2', 'ATTRIBUTE_3'])

    def top_bottom(df, sort_col):
        return df.sort_values(sort_col, ascending=False).head(5), df.sort_values(sort_col).head(5)

    top_sales, bottom_sales = top_bottom(combined, 'avg_sales_revenue')
    top_margin, bottom_margin = top_bottom(combined, 'avg_profit_margin')

    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        top_sales.to_csv(output_dir / "top_sales_segments.csv", index=False)
        bottom_sales.to_csv(output_dir / "bottom_sales_segments.csv", index=False)
        top_margin.to_csv(output_dir / "top_margin_segments.csv", index=False)
        bottom_margin.to_csv(output_dir / "bottom_margin_segments.csv", index=False)

    return top_sales, bottom_sales, top_margin, bottom_margin
