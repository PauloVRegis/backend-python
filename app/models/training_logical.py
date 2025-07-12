from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from .base import Base 
from datetime import datetime

class TrainingRegistration(Base):
    __tablename__ = "training_registration"
    
    id = Column(Integer, primary_key=True, index=True)
    training_id = Column(Integer, ForeignKey("trainings.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    professor_id = Column(Integer, ForeignKey("professors.id"))
    repetitions = Column(Integer)
    load = Column(Float)
    sets = Column(Integer)
    volume = Column(Float)
    intensity = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    user = relationship("User", back_populates="training_registration")
    professor = relationship("Professor", back_populates="training_registration")
    training = relationship("Training", back_populates="training_registration")