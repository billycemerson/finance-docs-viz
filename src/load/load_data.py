import pandas as pd
from supabase_client import get_supabase_client


def insert_fact(client, row):
    """
    Insert one row into fact_report table.
    Supabase will auto-generate 'id'.
    """
    fact_payload = {
        "company": row["company"],
        "day": int(row["day"]),
        "month": int(row["month"]),
        "year": int(row["year"]),
        "report_date": row["report_date"]
    }

    # Insert and return generated ID
    result = (
        client.table("fact_report")
        .insert(fact_payload)
        .execute()
    )

    return result.data[0]["id"]


def insert_dim_tables(client, fact_id, row):
    """
    Insert related dimension rows using the generated fact_id.
    """
    # Insert into dim_aset
    client.table("dim_aset").insert({
        "fact_id": fact_id,
        "kas": int(row["total_aset"]),
        "penempatan_pada_bank_indonesia": int(row["penempatan_pada_bank_indonesia"]),
        "kredit_yang_diberikan": int(row["kredit_yang_diberikan"]),
        "surat_berharga_yang_dimiliki": int(row["surat_berharga_yang_dimiliki"]),
        "total_aset": int(row["total_aset"])
    }).execute()

    # Insert into dim_liabilitas
    client.table("dim_liabilitas").insert({
        "fact_id": fact_id,
        "giro": int(row["giro"]),
        "tabungan": int(row["tabungan"]),
        "deposito": int(row["deposito"]),
        "total_liabilitas": int(row["total_liabilitas"])
    }).execute()

    # Insert into dim_ekuitas
    client.table("dim_ekuitas").insert({
        "fact_id": fact_id,
        "total_ekuitas": int(row["total_ekuitas"])
    }).execute()

    # Insert into dim_labarugi
    client.table("dim_labarugi").insert({
        "fact_id": fact_id,
        "pendapatan_bunga": int(row["pendapatan_bunga"]),
        "beban_bunga": int(row["beban_bunga"]),
        "pendapatan_beban_bunga_bersih": int(row["pendapatan_beban_bunga_bersih"]),
        "laba_rugi_bersih": int(row["laba_rugi_bersih"])
    }).execute()


def load_star_schema():
    """
    Load fact_report and dimension tables into Supabase.
    Fact table is inserted first, then its ID is used as FK.
    """
    client = get_supabase_client()

    fact_df = pd.read_csv("../../data/fact_report.csv")
    aset_df = pd.read_csv("../../data/dim_aset.csv")
    liab_df = pd.read_csv("../../data/dim_liabilitas.csv")
    ekuitas_df = pd.read_csv("../../data/dim_ekuitas.csv")
    labarugi_df = pd.read_csv("../../data/dim_labarugi.csv")

    for idx, fact_row in fact_df.iterrows():
        # Combine fact row and dims into one logical record
        record = {
            **fact_row,
            "total_aset": aset_df.loc[idx, "total_aset"],
            "kas": aset_df.loc[idx, "kas"],
            "penempatan_pada_bank_indonesia": aset_df.loc[idx, "penempatan_pada_bank_indonesia"],
            "kredit_yang_diberikan": aset_df.loc[idx, "kredit_yang_diberikan"],
            "surat_berharga_yang_dimiliki": aset_df.loc[idx, "surat_berharga_yang_dimiliki"],
            "giro": liab_df.loc[idx, "giro"],
            "tabungan": liab_df.loc[idx, "tabungan"],
            "deposito": liab_df.loc[idx, "deposito"],
            "total_liabilitas": liab_df.loc[idx, "total_liabilitas"],
            "total_ekuitas": ekuitas_df.loc[idx, "total_ekuitas"],
            "pendapatan_bunga": labarugi_df.loc[idx, "pendapatan_bunga"],
            "beban_bunga": labarugi_df.loc[idx, "beban_bunga"],
            "pendapatan_beban_bunga_bersih": labarugi_df.loc[idx, "pendapatan_beban_bunga_bersih"],
            "laba_rugi_bersih": labarugi_df.loc[idx, "laba_rugi_bersih"]
        }

        # Check if fact already exists
        exists = (
            client.table("fact_report")
            .select("*")
            .eq("company", record["company"])
            .eq("report_date", record["report_date"])
            .execute()
        )

        if exists.data:
            fact_id = exists.data[0]["id"]
        else:
            # Insert fact table first
            fact_id = insert_fact(client, record)

        # Insert dimension tables using fact_id
        insert_dim_tables(client, fact_id, record)

        print(f"Inserted fact_id={fact_id} for {record['company']} {record['report_date']}")

    print("Star-schema loading completed.")


if __name__ == "__main__":
    load_star_schema()