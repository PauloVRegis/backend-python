from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Exercise(Base):
    __tablename__ = "exercises"
    id      = Column(Integer, primary_key=True, index=True)
    name    = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    trainings = relationship("TrainingExercise", back_populates="exercise")
