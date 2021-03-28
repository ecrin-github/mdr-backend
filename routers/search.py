from fastapi import APIRouter

from models.request_bodies.search import StudyCharacteristicsModel, SpecificStudyModel, \
    SelectedStudyModel, ViaPublishedPaperModel
from general.study_extraction import get_by_study_characteristics, get_specific_study, \
    get_fetched_study, get_all_by_study_characteristics, get_all_specific_study
from general.object_extraction import get_fetched_data_objects, get_via_published_paper, \
    get_all_via_published_paper
from configs.types.identifier_types import IDENTIFIER_TYPES


router = APIRouter(
    prefix="/search",
    tags=["search"]
)


@router.post("/study-characteristics")
async def study_characteristics(request: StudyCharacteristicsModel) -> dict:

    results = await get_by_study_characteristics(
        title_contains=request.title_contains,
        logical_operator=request.logical_operator,
        topics_include=request.topics_include,
        filters=request.filters.studyFilters,
        page=int(request.page),
        size=int(request.page_size)
    )

    studies = results["hits"]["hits"]
    total = int(results["hits"]["total"]["value"])

    if total == 0:
        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page_size),
            "data": []
        }
    elif total == 1:
        study = studies[0]
        if study["_source"]["linked_data_objects"] is not None and len(
                study["_source"]["linked_data_objects"]) > 0:
            study["_source"]["linked_data_objects"] = await get_fetched_data_objects(
                study["_source"]["linked_data_objects"])
        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page_size),
            "data": [study["_source"]]
        }
    else:
        for study in studies:
            if study["_source"]["linked_data_objects"] is not None and len(
                    study["_source"]["linked_data_objects"]) > 0:
                study["_source"]["linked_data_objects"] = await get_fetched_data_objects(
                    study["_source"]["linked_data_objects"])
        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page),
            "data": [study["_source"] for study in studies]
        }


@router.post("/specific-study")
async def specific_study(request: SpecificStudyModel) -> dict:

    search_type = next((item for item in IDENTIFIER_TYPES if item["id"] == int(request.search_type)), None)
    search_type = search_type["name"]

    results = await get_specific_study(search_type=search_type,
                                 search_value=request.search_value,
                                 filters=request.filters.studyFilters,
                                 page=int(request.page),
                                 size=int(request.page_size))

    studies = results["hits"]["hits"]
    total = int(results["hits"]["total"]["value"])

    if total == 0:
        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page_size),
            "data": []
        }
    elif total == 1:
        study = studies[0]
        if study["_source"]["linked_data_objects"] is not None and len(
                study["_source"]["linked_data_objects"]) > 0:
            study["_source"]["linked_data_objects"] = await get_fetched_data_objects(
                study["_source"]["linked_data_objects"])
        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page_size),
            "data": [study["_source"]]
        }
    else:
        for study in studies:
            if study["_source"]["linked_data_objects"] is not None and len(
                    study["_source"]["linked_data_objects"]) > 0:
                study["_source"]["linked_data_objects"] = await get_fetched_data_objects(
                    study["_source"]["linked_data_objects"])

        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page_size),
            "data": [study["_source"] for study in studies]
        }


@router.post("/via-published-paper")
async def via_published_paper(request: ViaPublishedPaperModel) -> dict:

    results = await get_via_published_paper(search_type=request.search_type,
                                      search_value=request.search_value,
                                      filters=request.filters.objectFilters,
                                      page=int(request.page),
                                      size=int(request.page_size))

    total = int(results["hits"]["total"]["value"])
    data_objects = results["hits"]["hits"]

    if total == 0:
        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page_size),
            "data": []
        }
    elif total == 1:
        studies = []
        if data_objects[0]["_source"]["linked_studies"] is not None:
            study_id = data_objects[0]["_source"]["linked_studies"][0]
            study = await get_fetched_study(int(study_id))
            if study is not None:
                study["linked_data_objects"] = await get_fetched_data_objects(study["linked_data_objects"])
                studies.append(study)
        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page_size),
            "data": studies
        }
    else:
        studies = []
        for data_object in data_objects:
            if data_object["_source"]["linked_studies"] is not None and len(
                    data_object["_source"]["linked_studies"]) > 0:
                study_id = data_object["_source"]["linked_studies"][0]
                study = await get_fetched_study(int(study_id))
                if study is not None:
                    study["linked_data_objects"] = await get_fetched_data_objects(study["linked_data_objects"])
                    studies.append(study)
        return {
            "total": total,
            "current_page": int(request.page),
            "size": int(request.page_size),
            "data": studies
        }


@router.post("/all-study-characteristics")
async def all_study_characteristics(request: StudyCharacteristicsModel) -> list:

    results = await get_all_by_study_characteristics(title_contains=request.title_contains,
                                               logical_operator=request.logical_operator,
                                               topics_include=request.topics_include,
                                               filters=request.filters.studyFilters)

    studies = results["hits"]["hits"]
    total = int(results["hits"]["total"]["value"])

    if total == 0:
        return []
    elif total == 1:
        study = studies[0]
        if study["_source"]["linked_data_objects"] is not None and len(
                study["_source"]["linked_data_objects"]) > 0:
            study["_source"]["linked_data_objects"] = await get_fetched_data_objects(
                study["_source"]["linked_data_objects"])
        return [study["_source"]]
    else:
        for study in studies:
            if study["_source"]["linked_data_objects"] is not None and len(
                    study["_source"]["linked_data_objects"]) > 0:
                study["_source"]["linked_data_objects"] = await get_fetched_data_objects(
                    study["_source"]["linked_data_objects"])

        return [study["_source"] for study in studies]


@router.post("/all-specific-study")
async def all_specific_study(request: SpecificStudyModel) -> list:

    search_type = next((item for item in IDENTIFIER_TYPES if item["id"] == int(request.search_type)), None)
    search_type = search_type["name"]

    results = await get_all_specific_study(search_type=search_type,
                                     search_value=request.search_value,
                                     filters=request.filters.studyFilters)

    studies = results["hits"]["hits"]
    total = int(results["hits"]["total"]["value"])

    if total == 0:
        return []
    elif total == 1:
        study = studies[0]
        if study["_source"]["linked_data_objects"] is not None and len(
                study["_source"]["linked_data_objects"]) > 0:
            study["_source"]["linked_data_objects"] = await get_fetched_data_objects(
                study["_source"]["linked_data_objects"])
        return [study["_source"]]
    else:
        for study in studies:
            if study["_source"]["linked_data_objects"] is not None and len(
                    study["_source"]["linked_data_objects"]) > 0:
                study["_source"]["linked_data_objects"] = await get_fetched_data_objects(
                    study["_source"]["linked_data_objects"])
        return [study["_source"] for study in studies]


@router.post("/all-via-published-paper")
async def all_via_published_paper(request: ViaPublishedPaperModel) -> list:

    results = await get_all_via_published_paper(search_type=request.search_type,
                                          search_value=request.search_value,
                                          filters=request.filters.objectFilters)

    total = int(results["hits"]["total"]["value"])
    data_objects = results["hits"]["hits"]

    if total == 0:
        return []
    elif total == 1:
        studies = []
        if data_objects[0]["_source"]["linked_studies"] is not None:
            study_id = data_objects[0]["_source"]["linked_studies"][0]
            study = await get_fetched_study(int(study_id))
            if study is not None:
                study["linked_data_objects"] = await get_fetched_data_objects(study["linked_data_objects"])
                studies.append(study)
        return studies
    else:
        studies = []
        for data_object in data_objects:
            if data_object["_source"]["linked_studies"] is not None and len(
                    data_object["_source"]["linked_studies"]) > 0:
                study_id = data_object["_source"]["linked_studies"][0]
                study = await get_fetched_study(int(study_id))
                if study is not None:
                    study["linked_data_objects"] = await get_fetched_data_objects(study["linked_data_objects"])
                    studies.append(study)
        return studies


@router.post("/selected-study")
async def selected_study(request: SelectedStudyModel):

    result = await get_fetched_study(study_id=int(request.study_id))
    result['linked_data_objects'] = await get_fetched_data_objects(result['linked_data_objects'])

    if result is not None:
        return result
    else:
        return []
