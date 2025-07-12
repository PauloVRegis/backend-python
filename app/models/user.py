from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    trainings = relationship("Training", back_populates="users")
    training_registration = relationship("TrainingRegistration", back_populates="user")