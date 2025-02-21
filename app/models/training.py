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
    load = Column(Float) 
    volume = Column(Float)
    intensity = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
    user = relationship("User", back_populates="trainings")
    professor = relationship("Professor", back_populates="trainings")