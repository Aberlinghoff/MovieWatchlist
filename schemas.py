from pydantic import BaseModel, SecretStr
from datetime import datetime


# Auth schemas
class UserRegister(BaseModel):
    email: str
    username: str
    password: SecretStr

class UserResponse(BaseModel):
    email: str
    username: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: SecretStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# Watchlist schemas

class WatchlistAdd(BaseModel):
    movie_id: int

class WatchlistResponse(BaseModel):
    id: int
    movie_id: int
    created_at: datetime

    class Config:
        from_attributes = True