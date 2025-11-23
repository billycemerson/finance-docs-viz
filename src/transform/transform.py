import json
import pandas as pd

from clean_columns import clean_column_names
from clean_numeric import clean_numeric_columns
from handling_date import create_report_date
from schema_validation import validate_item

import warnings
warnings.filterwarnings("ignore")


def transform_star_schema():

    # Load extracted JSON
    with open("../../data/extracted_data.json", "r") as f:
        raw = json.load(f)

    # Validate using pydantic
    validated_raw = []
    for idx, item in enumerate(raw, start=1):
        if validate_item(item):
            validated_raw.append(item)
        else:
            print(f"Warning: invalid schema at index {idx}, skipping.")

    raw = validated_raw

    fact_rows = []
    aset_rows = []
    liab_rows = []
    ekuitas_rows = []
    labarugi_rows = []

    for idx, item in enumerate(raw, start=1):

        report_id = idx
        meta = item.get("metadata", {})
        data = item.get("data", {})

        # Fact table
        fact_rows.append({
            "report_id": report_id,
            "company": meta.get("company"),
            "day": meta.get("day"),
            "month": meta.get("month"),
            "year": meta.get("year"),
        })

        # Dimension: Aset
        aset_row = {"report_id": report_id}
        aset_row.update(data.get("aset", {}))
        aset_rows.append(aset_row)

        # Dimension: Liabilitas
        liab_row = {"report_id": report_id}
        liab_row.update(data.get("liabilitas", {}))
        liab_rows.append(liab_row)

        # Dimension: Ekuitas
        ek_row = {"report_id": report_id}
        ek_row.update(data.get("ekuitas", {}))
        ekuitas_rows.append(ek_row)

        # Dimension: Laba Rugi
        lr_row = {"report_id": report_id}
        lr_row.update(data.get("labarugi", {}))
        labarugi_rows.append(lr_row)

    # Convert to DataFrame
    fact_df = pd.DataFrame(fact_rows)
    aset_df = pd.DataFrame(aset_rows)
    liab_df = pd.DataFrame(liab_rows)
    ekuitas_df = pd.DataFrame(ekuitas_rows)
    labarugi_df = pd.DataFrame(labarugi_rows)

    # Clean all column names (including canonical synonym merge)
    fact_df = clean_column_names(fact_df)
    aset_df = clean_column_names(aset_df)
    liab_df = clean_column_names(liab_df)
    ekuitas_df = clean_column_names(ekuitas_df)
    labarugi_df = clean_column_names(labarugi_df)

    # Convert to numeric where applicable
    aset_df = clean_numeric_columns(aset_df, exclude=("report_id",))
    liab_df = clean_numeric_columns(liab_df, exclude=("report_id",))
    ekuitas_df = clean_numeric_columns(ekuitas_df, exclude=("report_id",))
    labarugi_df = clean_numeric_columns(labarugi_df, exclude=("report_id",))

    # Add report_date to the fact table
    fact_df = create_report_date(fact_df)

    # Save final star schema tables
    fact_df.to_csv("../../data/fact_report.csv", index=False)
    aset_df.to_csv("../../data/dim_aset.csv", index=False)
    liab_df.to_csv("../../data/dim_liabilitas.csv", index=False)
    ekuitas_df.to_csv("../../data/dim_ekuitas.csv", index=False)
    labarugi_df.to_csv("../../data/dim_labarugi.csv", index=False)

    print("Star schema transformation complete.")


if __name__ == "__main__":
    transform_star_schema()