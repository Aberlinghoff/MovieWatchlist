# Will need 3 endpoints:
#   POST /watchlist/ - add a movie to watchlist
#   GET /watchlist/ - get current user's watchlist
#   DELETE /watchlist/{movie_id} - remove a movie from watchlist
from typing import List

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from utils.auth import decode_token
from sqlalchemy.orm import Session
from database import get_db
from models import Watchlist
from schemas import WatchlistAdd, WatchlistResponse

router = APIRouter(
    prefix="/watchlist",
    tags=["watchlist"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token credentials")
    user_id = decode_token(token)
    if not user_id:
        raise credentials_exception
    return user_id

# POST /watchlist/
@router.post("/", response_model=WatchlistResponse, status_code=status.HTTP_201_CREATED)
def add_to_watchlist(watchlist_data: WatchlistAdd, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == user_id,
        Watchlist.movie_id == watchlist_data.movie_id
    ).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Movie already on watchlist")

    new_entry = Watchlist(user_id=user_id, movie_id=watchlist_data.movie_id)

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


# GET /watchlist/
@router.get("/", response_model=List[WatchlistResponse], status_code=status.HTTP_200_OK)
def get_watchlists(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Watchlist).filter(Watchlist.user_id == user_id).all()


# DELETE /watchlist/{movie_id}
@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_from_watchlist(movie_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Watchlist).filter(Watchlist.user_id == user_id, Watchlist.movie_id == movie_id).first()
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db.delete(existing)
    db.commit()