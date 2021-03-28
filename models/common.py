from pydantic import BaseModel


class FiltersList(BaseModel):
    studyFilters: list = []
    objectFilters: list = []
