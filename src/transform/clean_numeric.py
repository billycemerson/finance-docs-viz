import pandas as pd

def clean_numeric_columns(df, exclude=("company",)):
    """Convert financial fields to pure integers by removing dots."""
    for col in df.columns:
        if col not in exclude:
            df[col] = df[col].astype(str).str.replace(".", "", regex=False)
            df[col] = df[col].str.replace(",", "", regex=False)
            df[col] = pd.to_numeric(df[col], errors="ignore")
    return df