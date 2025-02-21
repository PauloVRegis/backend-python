from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base  # Importe a classe Base corretamente
from .training import Training

class Professor(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    users = relationship("User", back_populates="professor")
    trainings = relationship("Training", back_populates="professor")