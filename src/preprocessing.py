import pandas as pd
import numpy as np
from pathlib import Path

def preprocess_dataset(input_path, output_path):

    df = pd.read_excel(input_path)

    df['KEY'] = pd.to_numeric(df['KEY'], errors='coerce').fillna(-1).astype(int)

    def clean_currency(col):
        return pd.to_numeric(
            df[col].astype(str).str.replace(r'[$,]', '', regex=True),
            errors='coerce'
        )

    def clean_percentage(col):
        def parse_perc(x):
            if pd.isna(x):
                return np.nan
            if isinstance(x, str) and '%' in x:
                return float(x.replace('%', '')) / 100
            if isinstance(x, (int, float)) and x > 1:
                return x / 100
            return float(x)
        return df[col].apply(parse_perc)

    # Clean currency columns
    for curr_col in ['METRIC_1', 'METRIC_3', 'METRIC_4', 'METRIC_9']:
        df[curr_col] = round(clean_currency(curr_col), 2)

    # Clean percentage columns
    for perc_col in ['METRIC_2', 'METRIC_5', 'METRIC_6', 'METRIC_7', 'METRIC_8', 'METRIC_10']:
        df[perc_col] = round(clean_percentage(perc_col), 3)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    return df
