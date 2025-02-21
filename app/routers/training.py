from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.training import TrainingCreate, Training
from ..crud.training import create_training
from ..crud.training import get_training
from ..crud.user import get_user


router = APIRouter()

# Function to create training associating it with a user and a professor    
@router.post("/trainings/", response_model=Training)
def create_new_training(training: TrainingCreate = Body(...), db: Session = Depends(get_db)):
    user = get_user(db, user_id=training.user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")  
    professor = get_user(db, user_id=training.professor_id)
    if professor is None:
        raise HTTPException(status_code=404, detail="Professor não encontrado")  
    return create_training(db=db, training=training, user_id=training.user_id, professor_id=training.professor_id)

@router.get("/trainings/{training_id}/description", response_model=str)
def get_training_description(training_id: int, db: Session = Depends(get_db)):
    training = get_training(db, training_id=training_id)
    if training is None:
        raise HTTPException(status_code=404, detail="Treino não encontrado")
    return training.description  # Retorna apenas a descrição do treino