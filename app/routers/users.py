from fastapi import APIRouter, Depends
from ..schemas.user import User
from ..crud.user import get_user
from ..crud.user import create_user
from ..database import SessionLocal
from ..database import SessionLocal
from ..schemas.user import UserCreate
from sqlalchemy.orm import Session
from ..database.session import get_db

router = APIRouter()

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    db = SessionLocal()
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=User)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)