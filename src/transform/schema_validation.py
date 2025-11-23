from pydantic import BaseModel, ValidationError, RootModel
from typing import Dict, Optional


class MetadataModel(BaseModel):
    company: str
    day: int
    month: int
    year: int


# Generic dynamic section (aset, liabilitas, ekuitas, labarugi)
class SectionModel(RootModel[Dict[str, Optional[str]]]):
    pass


class DataModel(BaseModel):
    aset: SectionModel
    liabilitas: SectionModel
    ekuitas: SectionModel
    labarugi: SectionModel


class ExtractedItem(BaseModel):
    metadata: MetadataModel
    data: DataModel


def validate_item(item: dict) -> bool:
    """
    Validate a single extracted JSON item.
    Returns True if valid, False otherwise.
    """
    try:
        ExtractedItem(**item)
        return True
    except ValidationError as e:
        print("Schema error:", e)
        return False