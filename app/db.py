from typing import Generator
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import MONGO_URI, MONGO_DB_NAME, POSTGRES_URI

# --- MongoDB Setup ---
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]

def get_mongo_db():
    """Dependency function for getting the Mongo database instance."""
    return mongo_db


# --- PostgreSQL Setup ---
engine = create_engine(POSTGRES_URI, echo=True)  # echo=True to log SQL statements (optional)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_pg_db() -> Generator[Session, None, None]:
    """Dependency function for getting a SQLAlchemy Session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()