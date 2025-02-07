from fastapi import APIRouter, Depends, HTTPException
from ..schemas.user import UserCreate, User
from ..crud.user import create_user
from ..database import SessionLocal
from sqlalchemy.orm import Session
from ..database import get_db
from ..utils.security import get_password_hash

router = APIRouter()

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db=db, user=user)
    return db_user