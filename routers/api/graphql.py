from fastapi import APIRouter


router = APIRouter(
    prefix="/graphql/v1",
    tags=["graphql/v1"]
)
