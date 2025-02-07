from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.training import TrainingCreate, Training
from ..crud.training import create_training
from ..crud.training import get_training

router = APIRouter()

@router.post("/trainings/", response_model=Training)
def create_new_training(training: TrainingCreate, db: Session = Depends(get_db)):
    return create_training(db=db, training=training)

@router.get("/trainings/{training_id}/description", response_model=str)
def get_training_description(training_id: int, db: Session = Depends(get_db)):
    training = get_training(db, training_id=training_id)
    if training is None:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    return training.description  # Retorna apenas a descrição do treino