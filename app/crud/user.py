from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from ..schemas.professor import ProfessorCreate
from ..models.professor import Professor
from ..crud.professor import get_professor
from ..crud.professor import create_professor
from ..utils.security import get_password_hash

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password, professor_id=user.professor_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()