from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base  # Importe a classe Base corretamente

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    professor_id = Column(Integer, ForeignKey("professors.id"))

    professor = relationship("Professor", back_populates="users")