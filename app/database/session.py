from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base  # Importe a classe Base corretamente

# Defina a URL do banco de dados (SQLite neste exemplo)
DATABASE_URL = "sqlite:///./smart_force.db"

# Crie o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crie a fábrica de sessões (SessionLocal)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crie as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()