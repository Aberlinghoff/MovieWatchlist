# Functions that allow for searching through the TMDB for movies

import os
from dotenv import load_dotenv
import httpx

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')


def search_movies(query: str):

    url = "https://api.themoviedb.org/3/search/movie"
    search = httpx.get(url, params={"api_key": TMDB_API_KEY, "query": query})
    return search.json()["results"]