# api/main.py

from fastapi import FastAPI
from api.routes import students
from db.database import engine
from db.models import Base

app = FastAPI()

app.include_router(students.router)
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "EDPS is live!"}
