from fastapi import APIRouter, Depends
from ..schemas.professor import Professor
from ..crud.professor import get_professor
from ..crud.professor import create_professor
from ..schemas.professor import ProfessorCreate
from ..database import SessionLocal
from sqlalchemy.orm import Session
from ..database.session import get_db

router = APIRouter()

@router.get("/professors/{professor_id}", response_model=Professor)
def read_professor(professor_id: int):
    db = SessionLocal()
    professor = get_professor(db, professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor

@router.post("/professors/", response_model=Professor)
def create_new_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    return create_professor(db=db, professor=professor)