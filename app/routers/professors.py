from fastapi import APIRouter, Depends
from ..schemas.professor import Professor
from ..crud.professor import get_professor
from ..database import SessionLocal

router = APIRouter()

@router.get("/professors/{professor_id}", response_model=Professor)
def read_professor(professor_id: int):
    db = SessionLocal()
    professor = get_professor(db, professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor not found")
    return professor