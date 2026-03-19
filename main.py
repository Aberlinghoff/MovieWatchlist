from fastapi import FastAPI
from database import Base, engine
import models
from routers import auth, movies, watchlist

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Watchlist API")

app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(watchlist.router)