from pydantic import BaseModel
from typing import Optional

from models.common import FiltersList


class StudyCharacteristicsRestModel(BaseModel):
    title_contains: str
    logical_operator: str
    topics_include: str
    filters: Optional[FiltersList]
    page: Optional[int]
    page_size: Optional[int]


class SpecificStudyRestModel(BaseModel):
    search_type: int
    search_value: str
    filters: Optional[FiltersList]
    page: Optional[int]
    page_size: Optional[int]


class ViaPublishedPaperRestModel(BaseModel):
    search_type: str
    search_value: str
    filters: Optional[FiltersList]
    page: Optional[int]
    page_size: Optional[int]


class SelectedStudyRestModel(BaseModel):
    study_id: int
