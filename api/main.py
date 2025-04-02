# api/main.py

from fastapi import FastAPI
from api.routes import students

app = FastAPI()

app.include_router(students.router)

@app.get("/")
def root():
    return {"message": "EDPS is live!"}
