from pydantic import BaseModel
from datetime import datetime

class TrainingBase(BaseModel):
    name: str
    description: str
    student_id: int  # ID do aluno
    professor_id: int  # ID do professor

class TrainingCreate(TrainingBase):
    pass

class Training(TrainingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  