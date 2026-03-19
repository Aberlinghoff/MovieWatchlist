# Look up user by username - return 401 with "Invalid credentials" if not found
# Verify password against stored hash - return 401 with "invalid credentials" if fails
# Create JWT with create_token() and return with a 200

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import crud

from models import User
from schemas import UserLogin, UserRegister, TokenResponse, UserResponse
from database import get_db
from utils.auth import hash_password, verify_password, create_token, get_user_by_username, get_user_by_email

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Register new user
# POST /UserRegister/
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_register: UserRegister, db: Session = Depends(get_db)):
    existing_username = get_user_by_username(user_register.username, db)
    existing_email = get_user_by_email(user_register.email, db)
    if existing_username or existing_email:
        raise HTTPException(status_code=409, detail="Invalid credentials")
    hashed_password = hash_password(user_register.password)
    user = User(username=user_register.username, email=user_register.email, hashed_password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Login endpoint
# POST /UserLogin/
@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = get_user_by_username(user_login.username, db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_token(user.id)

    return {"access_token": access_token, "token_type": "bearer"}
