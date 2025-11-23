import re
import pandas as pd

# mapping for column names that have different wording but the same meaning
CANONICAL_MAP = {
    "laba_rugi_bersih_tahun_berjalan": "laba_rugi_bersih",
    "laba_rugi_bersih_periode_berjalan": "laba_rugi_bersih",
    "kredit_dan_pembiayaan_yang_diberikan": "kredit_yang_diberikan",
    "kredit_yang_diberikan": "kredit_yang_diberikan",
}

def clean_column_names(df):
    """Clean column names and merge fields with identical meaning."""
    cleaned = {}

    # Normalize column name patterns
    for col in df.columns:
        new_col = col.replace("metadata.", "").replace("data.", "")
        new_col = new_col.lower()
        new_col = re.sub(r'[^a-z0-9]+', '_', new_col).strip('_')

        cleaned[col] = new_col

    df = df.rename(columns=cleaned)

    # Apply canonical rename for synonym columns
    for original, canonical in CANONICAL_MAP.items():
        if original in df.columns:
            df = df.rename(columns={original: canonical})

    # Merge duplicate canonical columns produced by renaming
    df = _merge_duplicate_synonym_columns(df, CANONICAL_MAP)

    return df


def _merge_duplicate_synonym_columns(df, canonical_map):
    """
    Merge synonym columns by filling non-null values from left to right.
    Ensures only one final canonical column remains.
    """
    target_columns = set(canonical_map.values())

    for target in target_columns:
        matching_cols = [c for c in df.columns if c == target]

        if len(matching_cols) <= 1:
            continue

        # Fill missing values using left-to-right non-null values
        df[target] = df[matching_cols].bfill(axis=1).iloc[:, 0]

        # Remove duplicate columns after merging
        df = df.loc[:, ~df.columns.duplicated()]

    return df