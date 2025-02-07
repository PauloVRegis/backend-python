from sqlalchemy.orm import Session
from ..models.training import Training
from ..schemas.training import TrainingCreate

def create_training(db: Session, training: TrainingCreate):
    db_training = Training(
        name=training.name,
        description=training.description,
        student_id=training.student_id,
        professor_id=training.professor_id
    )
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training

def get_training(db: Session, training_id: int):
    return db.query(Training).filter(Training.id == training_id).first()