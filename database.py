from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connection string that points to SQLite file
DATABASE_URL = "sqlite:///./recipes.db"

# Tell SQLite to allow FastAPI to run on multiple threads
engine= create_engine(
    DATABASE_URL,connect_args={"check_same_thread": False}
)

# autocommit=False -> changes won't save until explicitly committed
# autoflush=False -> SQLAlchemy won't auto-push changes mid-session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is class database models inherit from
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()