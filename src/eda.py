import pandas as pd

def analyze_dataset(df):
    results = {'Metric': [], 'Value': []}

    results['Metric'].append('Total rows')
    results['Value'].append(len(df))
    results['Metric'].append('Distinct KEYs')
    results['Value'].append(df['KEY'].nunique())
    results['Metric'].append('Duplicate KEYs')
    results['Value'].append(df['KEY'].duplicated().sum())

    missing = df.isna().sum()
    for col, val in missing.items():
        if val > 0:
            results['Metric'].append(f'Missing values in {col}')
            results['Value'].append(val)

    return pd.DataFrame(results)

def metric_analysis(df):
    metric_cols = [col for col in df.columns if col.startswith('METRIC_')]
    avg_metrics_per_key = df.groupby('KEY')[metric_cols].mean()
    avg_metrics_per_key['avg_metric'] = round(avg_metrics_per_key.mean(axis=1), 2)
    return avg_metrics_per_key.reset_index()

def summary_statistics(df):
    metric_cols = [col for col in df.columns if col.startswith('METRIC_')]
    summ_df = df[metric_cols]
    return round(summ_df.describe(include='all').transpose(), 2)

def detect_outliers(df, cat_threshold_pct=5):
    metric_cols = [c for c in df.columns if c.startswith('METRIC_')]
    cat_cols = [c for c in df.columns if c.startswith('ATTRIBUTE_')]

    total_rows = len(df)
    outlier_data = []

    for col in metric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outlier_count = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col].count()
        outlier_pct = (outlier_count / total_rows) * 100

        outlier_data.append({
            'Metric': col,
            'Outlier Count': outlier_count,
            'Outlier Percentage (%)': round(outlier_pct, 2),
            'Outlier Type': 'numeric'
        })

    for col in cat_cols:
        counts = df[col].value_counts(dropna=False)
        counts_pct = counts / total_rows * 100
        rare_cats = counts_pct[counts_pct < cat_threshold_pct]

        if not rare_cats.empty:
            outlier_data.append({
                'Metric': col,
                'Outlier Count': int(rare_cats.sum()),
                'Outlier Percentage (%)': round(rare_cats.sum() / total_rows * 100, 2),
                'Outlier Type': 'categorical',
            })
        else:
            outlier_data.append({
                'Metric': col,
                'Outlier Count': 0,
                'Outlier Percentage (%)': 0.0,
                'Outlier Type': 'categorical',
            })

    return pd.DataFrame(outlier_data)
