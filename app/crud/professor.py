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
    """Get professor by ID"""
    return db.query(Professor).filter(Professor.id == professor_id).first()

def get_professors(db: Session, skip: int = 0, limit: int = 100):
    """Get all professors with pagination"""
    return db.query(Professor).offset(skip).limit(limit).all()