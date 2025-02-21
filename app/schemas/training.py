from pydantic import BaseModel
from datetime import datetime

class TrainingBase(BaseModel):
    name: str
    description: str
    user_id: int  # 💡 Confirme que está definido aqui
    professor_id: int  # 💡 Confirme que está definido aqui
    repetitions: int
    sets: int
    load: float

class TrainingCreate(TrainingBase):
    pass

class Training(TrainingBase):
    id: int
    volume: float
    intensity: float
    created_at: datetime

    class Config:
        from_attributes = True
