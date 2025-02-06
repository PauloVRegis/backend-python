from fastapi import APIRouter, Depends
from ..schemas.user import User
from ..crud.user import get_user
from ..database import SessionLocal

router = APIRouter()

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    db = SessionLocal()
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user