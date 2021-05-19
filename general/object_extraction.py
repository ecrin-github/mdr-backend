from typing import List
from elasticsearch import AsyncElasticsearch
from configs.es_configs import ELASTICSEARCH_HOST, OBJECT_INDEX_NAME


es = AsyncElasticsearch(hosts=[ELASTICSEARCH_HOST])


async def get_fetched_data_objects(data_object_ids: List[int]) -> list:

    size = len(data_object_ids)

    query_body = {
        "size": size,
        "query": {
            "bool": {
                "filter": [{
                    "terms": {
                        "id": data_object_ids
                    }
                }]
            }
        }
    }

    result = await es.search(index=OBJECT_INDEX_NAME, body=query_body)

    linked_data_objects = []

    if len(result['hits']['hits']) > 0:
        for data_object in result['hits']['hits']:
            linked_data_objects.append(data_object['_source'])

    return linked_data_objects


async def get_via_published_paper(search_type: str, search_value: str, filters: list, page: int, size: int) -> dict:

    query_body = {}

    start_from = ((page + 1) * size) - size

    if start_from == 1 and size == 1:
        start_from = 0

    if search_type == "doi":
        query_body = {
            "from": start_from,
            "size": size,
            "query": {
                "bool": {
                    "must": {
                        "term": {
                            "doi": search_value
                        }
                    },
                    "must_not": filters
                },
            }
        }

    elif search_type == "title":

        query_body = {
            "from": start_from,
            "size": size,
            "query": {
                "bool": {
                    "must": [{
                        "bool": {
                            "should": [{
                                "simple_query_string": {
                                    "query": search_value,
                                    "fields": ["display_title"],
                                    "default_operator": "and",
                                },
                            }, {
                                "nested": {
                                    "path": "object_titles",
                                    "query": {
                                        "simple_query_string": {
                                            "query": search_value,
                                            "fields": ["object_titles.title_text"],
                                            "default_operator": "and",
                                        },
                                    },
                                },
                            }],
                            "minimum_should_match": 1,
                        },
                    }],
                    "must_not": filters
                }
            }
        }

    result = await es.search(index=OBJECT_INDEX_NAME, body=query_body)

    return result


async def get_all_via_published_paper(search_type: str, search_value: str, filters: list) -> dict:

    query_body = {}

    if search_type == "doi":
        query_body = {
            "size": 10000,
            "query": {
                "bool": {
                    "must": {
                        "term": {
                            "doi": search_value
                        }
                    },
                    "must_not": filters
                },
            }
        }

    elif search_type == "title":

        query_body = {
            "size": 10000,
            "query": {
                "bool": {
                    "must": [{
                        "bool": {
                            "should": [{
                                "simple_query_string": {
                                    "query": search_value,
                                    "fields": ["display_title"],
                                    "default_operator": "and",
                                },
                            }, {
                                "nested": {
                                    "path": "object_titles",
                                    "query": {
                                        "simple_query_string": {
                                            "query": search_value,
                                            "fields": ["object_titles.title_text"],
                                            "default_operator": "and",
                                        },
                                    },
                                },
                            }],
                            "minimum_should_match": 1,
                        },
                    }],
                    "must_not": filters
                }
            }
        }

    result = await es.search(index=OBJECT_INDEX_NAME, body=query_body)

    return result
