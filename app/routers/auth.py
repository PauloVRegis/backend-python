from fastapi import APIRouter, Depends, HTTPException
from ..schemas.user import UserCreate
from ..crud.user import create_user
from ..database import SessionLocal
from ..utils.security import get_password_hash

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    db = SessionLocal()
    db_user = create_user(db, user)
    return db_user