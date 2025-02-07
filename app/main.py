from fastapi import FastAPI
from .routers import users, professors, training
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(professors.router)
app.include_router(training.router)

@app.get("/")  
def read_root():
    return {"message": "Bem vindo ao SmartForce!"}