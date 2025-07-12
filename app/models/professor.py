from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    trainings = relationship("Training", back_populates="professor")
    training_registration = relationship("TrainingRegistration", back_populates="professor")