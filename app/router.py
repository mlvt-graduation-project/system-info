from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_pg_db, get_mongo_db
from app.services.mongo_service import get_all_items
from app.services.postgres_service import get_all_users

router = APIRouter()

@router.get("/items")
def read_items(mongo_db = Depends(get_mongo_db)):
    """
    Retrieve items from MongoDB using the 'items' collection.
    """
    return get_all_items(mongo_db)

@router.get("/users")
def read_users(db: Session = Depends(get_pg_db)):
    """
    Retrieve all users from PostgreSQL.
    """
    return get_all_users(db)