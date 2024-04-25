# routers/admin/lesson_questions.py

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from typing import Annotated
import database.models as models
from database.database import SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]