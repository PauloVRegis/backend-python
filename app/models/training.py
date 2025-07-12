from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .base import Base 
from datetime import datetime

class Training(Base): 
    __tablename__ = "trainings" 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    professor_id = Column(Integer, ForeignKey("professors.id"))
    repetitions = Column(Integer)
    sets = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)
    users = relationship("User", back_populates="trainings")
    professor = relationship("Professor", back_populates="trainings")
    training_registration = relationship("TrainingRegistration", back_populates="training")
    training_exercises = relationship("TrainingExercise", back_populates="training")

class TrainingExercise(Base):
    __tablename__ = "training_exercises"

    id          = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    repetitions = Column(Integer)
    sets        = Column(Integer)

    training    = relationship("Training", back_populates="training_exercises")
    exercise    = relationship("Exercise", back_populates="trainings")