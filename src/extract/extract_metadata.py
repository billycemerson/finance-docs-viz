import pdfplumber
import re
import os

def extract_text_from_pdf(file_path: str) -> str:
    """Read the first page of a PDF file and return extracted text."""
    with pdfplumber.open(file_path) as pdf:
        first_page = pdf.pages[0]
        return first_page.extract_text()


def extract_company_name_from_path(file_path: str) -> str | None:
    """
    Extract company name from subfolder name.
    Example:
    '../../data/downloads/bca/Agustus 2024.pdf' -> 'bca'
    '../../data/downloads/btn/Agustus 2024.pdf' -> 'btn'
    """
    parts = file_path.replace("\\", "/").split("/")
    # Search folder name inside downloads/
    for i, part in enumerate(parts):
        if part == "downloads" and i + 1 < len(parts):
            return parts[i + 1]  # folder right after 'downloads'
    return None


def extract_report_date(text: str) -> dict | None:
    """
    Extract date information from text.
    Handles:
    - 'Pada tanggal 31 Mei 2024'
    - 'Per 31 Agustus 2024'
    - 'TANGGAL LAPORAN : 31 JANUARI 2024'
    """
    text_lower = text.lower()

    patterns = [
        r"pada tanggal (\d{1,2}) (\w+) (\d{4})",
        r"per (\d{1,2}) (\w+) (\d{4})",
        r"tanggal laporan\s*:\s*(\d{1,2}) (\w+) (\d{4})",
    ]

    match = None
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            break

    if not match:
        return None

    day = int(match.group(1))
    month_name = match.group(2)
    year = int(match.group(3))

    month_map = {
        "januari": 1, "februari": 2, "maret": 3, "april": 4,
        "mei": 5, "juni": 6, "juli": 7, "agustus": 8,
        "september": 9, "oktober": 10, "november": 11, "desember": 12
    }

    month_number = month_map.get(month_name.lower())

    return {
        "day": day,
        "month": month_number,
        "month_name": month_name.capitalize(),
        "year": year
    }


def extract_metadata(file_path: str) -> dict:
    """Main function to extract all metadata fields from the PDF."""
    text = extract_text_from_pdf(file_path)

    company = extract_company_name_from_path(file_path)
    date_info = extract_report_date(text)

    metadata = {
        "company": company,
        "day": date_info.get("day") if date_info else None,
        "month": date_info.get("month") if date_info else None,
        "month_name": date_info.get("month_name") if date_info else None,
        "year": date_info.get("year") if date_info else None,
    }

    return metadata


# Example Usage
# pdf_path = "../../data/downloads/bni/LKP_BLN_2024-01_New-SEOJK9_IND.pdf"
# metadata = extract_metadata(pdf_path)
# print(metadata)