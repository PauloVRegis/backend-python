from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True