from sqlalchemy.orm import Session
from ..models.professor import Professor
from ..schemas.professor import ProfessorCreate


def create_professor(db: Session, professor: ProfessorCreate):
    db_professor = Professor(name=professor.name)
    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)
    return db_professor

def get_professor(db: Session, professor_id: int):
    return db.query(Professor).filter(Professor.id == professor_id).first()