from fastapi import APIRouter


router = APIRouter(
    prefix="/graphql",
    tags=["graphql"]
)
