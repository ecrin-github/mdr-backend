from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import search
from routers.api import rest, es_query_based, graphql

from elasticsearch import AsyncElasticsearch
from configs.es_configs import ELASTICSEARCH_HOST


app = FastAPI()
es = AsyncElasticsearch(hosts=[ELASTICSEARCH_HOST])


origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.include_router(search.router)
app.include_router(rest.router)
app.include_router(es_query_based.router)
app.include_router(graphql.router)


@app.on_event("shutdown")
async def app_shutdown():
    await es.close()