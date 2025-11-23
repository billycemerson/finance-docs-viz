import camelot
import pandas as pd

def detect_flavor_from_path(file_path: str) -> str:
    """
    Detect Camelot flavor based on folder name.
    Default = lattice
    """
    lower_path = file_path.lower()
    if "bca" in lower_path:
        return "stream"
    if "btn" in lower_path:
        return "hybrid"
    if "bni" in lower_path:
        return "hybrid"
    return "lattice"


def read_tables(file_path: str):
    """Read PDF and return Camelot tables with auto-selected flavor"""
    flavor = detect_flavor_from_path(file_path)
    print(f"Using flavor: {flavor}")

    tables = camelot.read_pdf(file_path, flavor=flavor, pages="all", split_text=True)

    # for t in tables:
    #     print(t.df)             # Print table dataframe
    #     print(t.parsing_report) # Parsing report for debugging

    return tables


def extract_values_from_tables(tables, target_fields):
    """Extract required fields from Camelot tables and return dict"""
    results = {field: None for field in target_fields}  # prefill keys

    for tbl in tables:
        df = tbl.df

        for field in target_fields:
            mask = df.map(lambda x: str(x).lower().strip()).isin([field.lower().strip()])

            if mask.any().any():
                row_index = mask.any(axis=1).idxmax()
                col_index = mask.any(axis=0).idxmax()

                value_col = col_index + 1
                if value_col < df.shape[1]:
                    results[field] = df.iat[row_index, value_col]

    return results

def extract_all_financial_data(file_path):
    """Extract all financial data in one PDF processing"""
    tables = read_tables(file_path)
    
    # Define all target fields
    aset_fields = ["kas", "penempatan pada bank indonesia", "kredit yang diberikan", 
                   "kredit dan pembiayaan yang diberikan", "surat berharga yang dimiliki", "total aset"]
    
    liabilitas_fields = ["giro", "tabungan", "deposito", "total liabilitas"]
    
    ekuitas_fields = ["total ekuitas"]
    
    labarugi_fields = ["pendapatan bunga", "beban bunga", "pendapatan (beban) bunga bersih", 
                       "laba (rugi) bersih tahun berjalan", "laba (rugi) bersih periode berjalan"]
    
    # Extract all data
    aset_data = extract_values_from_tables(tables, aset_fields)
    liabilitas_data = extract_values_from_tables(tables, liabilitas_fields)
    ekuitas_data = extract_values_from_tables(tables, ekuitas_fields)
    labarugi_data = extract_values_from_tables(tables, labarugi_fields)
    
    return {
        "aset": aset_data,
        "liabilitas": liabilitas_data,
        "ekuitas": ekuitas_data,
        "labarugi": labarugi_data
    }

# Example Usage
# pdf_path = "../../data/downloads/bni/LKP_BLN_2024-01_New-SEOJK9_IND.pdf"
# financial_data = extract_all_financial_data(pdf_path)
# print(financial_data)