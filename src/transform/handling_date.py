import pandas as pd

def create_report_date(df):
    """Create proper datetime from year + month."""
    df["report_date"] = pd.to_datetime(
        df["year"].astype(int).astype(str) + "-" + df["month"].astype(int).astype(str) + "-01"
    ) + pd.offsets.MonthEnd(1)
    return df