from sqlalchemy.orm import Session
from ..models.training import Training
from ..schemas.training import TrainingCreate
from ..models.user import User
from ..models.professor import Professor

# Create training associating it with a user
def create_training(db: Session, training: TrainingCreate, user_id: int, professor_id: int):
    user = db.query(User).filter(User.id == training.user_id).first()
    professor = db.query(User).filter(User.id == training.professor_id).first()
    if not user:
        raise ValueError("Usuário não encontrado")
    db_training = Training(**training.model_dump())
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training

def get_training(db: Session, training_id: int):
    return db.query(Training).filter(Training.id == training_id).first()