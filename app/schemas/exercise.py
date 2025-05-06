from pydantic import BaseModel
from datetime import datetime

class ExerciseBase(BaseModel):
    name: str
    description: str
    muscle_group: str

   

class ExerciseCreate(ExerciseBase):
    pass

    class Config:
        from_attributes = True