from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Training(Base):
    __tablename__ = "trainings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    student_id = Column(Integer, ForeignKey("users.id"))  # Atrelado a um aluno
    professor_id = Column(Integer, ForeignKey("professors.id"))  # Criado por um professor
    created_at = Column(DateTime, default=datetime.now)
    student = relationship("User", back_populates="trainings")
    professor = relationship("Professor", back_populates="trainings")