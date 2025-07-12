from pydantic import BaseModel
from datetime import datetime

class ProfessorBase(BaseModel):
    name: str

class ProfessorCreate(ProfessorBase):
    pass

class Professor(ProfessorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True