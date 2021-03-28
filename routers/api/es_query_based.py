from fastapi import APIRouter, Body
from elasticsearch import AsyncElasticsearch

from configs.es_configs import ELASTICSEARCH_HOST, STUDY_INDEX_NAME, OBJECT_INDEX_NAME
from general.study_extraction import get_fetched_study
from general.object_extraction import get_fetched_data_objects


es = AsyncElasticsearch(hosts=[ELASTICSEARCH_HOST])

router = APIRouter(
    prefix="/es-query-based",
    tags=["es-query-based"]
)


@router.post("/studies")
async def es_query_get_studies(request: dict = {}) -> dict:

    results = await es.search(index=STUDY_INDEX_NAME, body=request)
    
    studies = results["hits"]["hits"]
    total = int(results["hits"]["total"]["value"])

    if total == 0:
        return {
            "total": total,
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
            "data": [study["_source"] for study in studies]
        }


@router.post("/objects")
async def es_query_get_objects(request: dict = {}) -> dict:

    results = await es.search(index=OBJECT_INDEX_NAME, body=request.body)

    total = int(results["hits"]["total"]["value"])
    data_objects = results["hits"]["hits"]

    if total == 0:
        return {
            "total": total,
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
            "data": studies
        }
