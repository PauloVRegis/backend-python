from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.models import Teacher

router = APIRouter()

@router.post("/teachers/")
def create_teacher(first_name: str, last_name: str, db: Session = Depends(get_db)):
    teacher = Teacher(first_name=first_name, last_name=last_name)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher