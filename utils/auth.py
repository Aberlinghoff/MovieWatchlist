# Hash plain text password
# Verify a plain text password against stored hash
# Create JWT (encoding user_id and expiry)
# Decode incoming JWT to get user_id

from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models import User

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))



# set bcrypt as hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_token(user_id):
    expiry = datetime.now(datetime.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expiry}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token):
    try:
        decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decode.get("sub")
    except JWTError:
        return None

def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()