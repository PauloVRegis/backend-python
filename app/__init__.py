from fastapi import FastAPI
from .database import SessionLocal, engine
from .models.base import Base  # Importe a classe Base corretamente

# Cria as tabelas no banco de dados (se não existirem)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Importe e inclua os roteadores
from .routers import  users, professors

app.include_router(users.router)
app.include_router(professors.router)