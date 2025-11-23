import os
import json
from extract_data import extract_all_financial_data
from extract_metadata import extract_metadata

import warnings

# To ignore all warnings
warnings.simplefilter('ignore')

def extract():
    # Path to the folder containing PDF files (will include subfolders)
    folder_path = "../../data/downloads"

    # Prepare output file path and ensure output directory exists
    output_path = "../../data/extracted_data.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    all_results = []  # Collect all file results

    # Walk through folder and all subfolders
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Process only PDF files
            if not filename.lower().endswith(".pdf"):
                continue

            pdf_path = os.path.join(root, filename)
            rel_source = os.path.relpath(root, folder_path)  # subfolder name (e.g., 'bca' or 'btn')
            print(f"\nProcessing: {os.path.join(rel_source, filename)}")

            try:
                # Extract financial table values using Camelot
                data_results = extract_all_financial_data(pdf_path)

                # Extract company name and reporting date using pdfplumber
                metadata = extract_metadata(pdf_path)

                # Combine the output for this file
                result = {
                    "file": filename,
                    "source_folder": rel_source,
                    "metadata": metadata,
                    "data": data_results
                }

                # Append to master list
                all_results.append(result)

                # Optional: print single-file result to console
                print(result)

            except Exception as e:
                # If one file fails, log and continue with next file
                print(f"Error processing {filename} in {rel_source}: {e}")
                # Optionally append an error record instead of skipping:
                # all_results.append({"file": filename, "source_folder": rel_source, "error": str(e)})

    # Save all results as a JSON array
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)

    print(f"\nSaved {len(all_results)} records to {output_path}")

if __name__ == "__main__":
    extract()