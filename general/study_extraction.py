from elasticsearch import AsyncElasticsearch
from configs.es_configs import ELASTICSEARCH_HOST, STUDY_INDEX_NAME


es = AsyncElasticsearch(hosts=[ELASTICSEARCH_HOST])


async def get_fetched_study(study_id: int):

    query_body = {
        "size": 1,
        "query": {
            "term": {
                "id": study_id
            }
        }
    }

    result = await es.search(index=STUDY_INDEX_NAME, body=query_body)

    if len(result['hits']['hits']) > 0:
        return result['hits']['hits'][0]['_source']
    else:
        return None


async def get_specific_study(search_type: str, search_value: str, filters: list, page: int, size: int) -> dict:

    start_from = ((page + 1) * size) - size

    if start_from == 1 and size == 1:
        start_from = 0

    query_body = {
        "from": start_from,
        "size": size,
        "query": {
            "bool": {
                "must": {
                    "nested": {
                        "path": "study_identifiers",
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        "term": {
                                            'study_identifiers.identifier_type': search_type,
                                        },
                                    },
                                    {
                                        "term": {
                                            'study_identifiers.identifier_value': search_value
                                        }
                                    }
                                ],
                            },
                        }
                    }
                },
                "must_not": filters,
            },
        }
    }

    result = await es.search(index=STUDY_INDEX_NAME, body=query_body)

    return result


async def get_by_study_characteristics(title_contains: str, logical_operator: str, topics_include: str, filters: list, page: int, size: int) -> dict:

    if logical_operator == "and":
        query_condition = "must"
    else:
        query_condition = "should"

    start_from = ((page + 1) * size) - size

    if start_from == 1 and size == 1:
        start_from = 0

    query_body = {
        "from": start_from,
        "size": size,
        "query": {
            "bool": {
                query_condition: [{
                    "bool": {
                        "should": [{
                            "simple_query_string": {
                                "query": title_contains,
                                "fields": ["display_title"],
                                "default_operator": "and"
                            }
                        }, {
                            "nested": {
                                "path": "study_titles",
                                "query": {
                                    "simple_query_string": {
                                        "query": title_contains,
                                        "fields": ["study_titles.title_text"],
                                        "default_operator": "and"
                                    }
                                }
                            }
                        }]
                    }
                }],
                "must_not": filters,
            }
        }
    }

    if topics_include is not None and topics_include != '':
        query_body['query']['bool'][query_condition].append({
            "nested": {
                "path": 'study_topics',
                "query": {
                    "simple_query_string": {
                        "query": topics_include,
                        "fields": ['study_topics.topic_value'],
                        "default_operator": "and",
                    },
                },
            },
        })

    result = await es.search(index=STUDY_INDEX_NAME, body=query_body)

    return result


async def get_all_specific_study(search_type: str, search_value: str, filters: list) -> dict:

    query_body = {
        "size": 10000,
        "query": {
            "bool": {
                "must": {
                    "nested": {
                        "path": "study_identifiers",
                        "query": {
                            "bool": {
                                "must": [
                                    {
                                        "term": {
                                            'study_identifiers.identifier_type': search_type,
                                        },
                                    },
                                    {
                                        "term": {
                                            'study_identifiers.identifier_value': search_value
                                        }
                                    }
                                ],
                            },
                        }
                    }
                },
                "must_not": filters,
            },
        }
    }

    result = await es.search(index=STUDY_INDEX_NAME, body=query_body)

    return result


async def get_all_by_study_characteristics(title_contains: str, logical_operator: str, topics_include: str, filters: str) -> dict:

    if logical_operator == "and":
        query_condition = "must"
    else:
        query_condition = "should"

    query_body = {
        "size": 10000,
        "query": {
            "bool": {
                query_condition: [{
                    "bool": {
                        "should": [{
                            "simple_query_string": {
                                "query": title_contains,
                                "fields": ["display_title"],
                                "default_operator": "and"
                            }
                        }, {
                            "nested": {
                                "path": "study_titles",
                                "query": {
                                    "simple_query_string": {
                                        "query": title_contains,
                                        "fields": ["study_titles.title_text"],
                                        "default_operator": "and"
                                    }
                                }
                            }
                        }]
                    }
                }],
                "must_not": filters,
            }
        }
    }

    if topics_include is not None and topics_include != '':
        query_body['query']['bool'][query_condition].append({
            "nested": {
                "path": 'study_topics',
                "query": {
                    "simple_query_string": {
                        "query": topics_include,
                        "fields": ['study_topics.topic_value'],
                        "default_operator": "and",
                    },
                },
            },
        })

    result = await es.search(index=STUDY_INDEX_NAME, body=query_body)

    return result
