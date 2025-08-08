from fastapi import APIRouter, Depends
from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.user import User
from app.schemas.user import UserOut
from typing import List

router = APIRouter()

@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users