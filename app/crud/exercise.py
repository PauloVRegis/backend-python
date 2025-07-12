from sqlalchemy.orm import Session
from ..models.exercise import Exercise
from ..schemas.exercise import ExerciseCreate

def create_exercise(db: Session, exercise: ExerciseCreate):
    """Create a new exercise"""
    db_exercise = Exercise(**exercise.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise

def get_exercise(db: Session, exercise_id: int):
    """Get exercise by ID"""
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()

def get_exercises(db: Session, skip: int = 0, limit: int = 100):
    """Get all exercises with pagination"""
    return db.query(Exercise).offset(skip).limit(limit).all()

def get_exercises_by_name(db: Session, name: str, skip: int = 0, limit: int = 100):
    """Get exercises by name (partial match)"""
    return db.query(Exercise).filter(Exercise.name.ilike(f"%{name}%")).offset(skip).limit(limit).all()

def update_exercise(db: Session, exercise_id: int, exercise_update: ExerciseCreate):
    """Update an exercise"""
    db_exercise = get_exercise(db, exercise_id)
    if db_exercise:
        for key, value in exercise_update.model_dump().items():
            setattr(db_exercise, key, value)
        db.commit()
        db.refresh(db_exercise)
    return db_exercise

def delete_exercise(db: Session, exercise_id: int):
    """Delete an exercise"""
    db_exercise = get_exercise(db, exercise_id)
    if db_exercise:
        db.delete(db_exercise)
        db.commit()
        return True
    return False 