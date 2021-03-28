from pydantic import BaseModel
from typing import Optional

from models.common import FiltersList


class StudyCharacteristicsModel(BaseModel):
    title_contains: str
    logical_operator: str
    topics_include: str
    filters: FiltersList
    page: Optional[int]
    page_size: Optional[int]


class SpecificStudyModel(BaseModel):
    search_type: int
    search_value: str
    filters: FiltersList
    page: Optional[int]
    page_size: Optional[int]


class ViaPublishedPaperModel(BaseModel):
    search_type: str
    search_value: str
    filters: FiltersList
    page: Optional[int]
    page_size: Optional[int]


class SelectedStudyModel(BaseModel):
    study_id: int
