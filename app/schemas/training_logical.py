from pydantic import BaseModel
from datetime import datetime

class TrainingRegistrationBase(BaseModel):
    name: str
    description: str
    user_id: int  # 💡 Confirme que está definido aqui
    professor_id: int  # 💡 Confirme que está definido aqui
    repetitions: int
    volume: float
    intensity: float
    load: float
    sets: int

class TrainingRegistrationCreate(TrainingRegistrationBase):
    pass

class TrainingRegistration(TrainingRegistrationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
