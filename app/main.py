from fastapi import FastAPI
from .routers import users, professors

app = FastAPI()

app.include_router(users.router)
app.include_router(professors.router)

@app.get("/")  
def read_root():
    return {"message": "Bem vindo ao SmartForce!"}