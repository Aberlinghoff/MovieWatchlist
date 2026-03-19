# One GET endpoint at "/search" that accepts a query str param, returns results from search_movies()

from fastapi import APIRouter
from utils.tmdb import search_movies

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)

@router.get("/search")
def search(query: str):
    return search_movies(query)
