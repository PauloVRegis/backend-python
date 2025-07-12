from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TrainingExerciseBase(BaseModel):
    exercise_id: int
    sets: int
    repetitions: int

class TrainingExerciseCreate(TrainingExerciseBase):
    pass

class TrainingExercise(TrainingExerciseBase):
    id: int
    exercise_name: Optional[str] = None
    exercise_description: Optional[str] = None

    class Config:
        from_attributes = True

class TrainingBase(BaseModel):
    name: str
    description: Optional[str] = None
    user_id: int
    professor_id: int

class TrainingCreate(TrainingBase):
    exercises: List[TrainingExerciseCreate]

class Training(TrainingBase):
    id: int
    created_at: datetime
    exercises: List[TrainingExercise] = []

    class Config:
        from_attributes = True

class TrainingResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    user_id: int
    professor_id: int
    created_at: datetime
    exercises: List[TrainingExercise] = []

    class Config:
        from_attributes = True
