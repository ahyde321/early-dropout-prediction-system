# api/main.py

from fastapi import FastAPI
from api.routes import prediction, students, uploads, admin, auth
from db.database import engine
from db.models import Base
import os

app = FastAPI()

FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:8080')  # Default to local if not specified

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(prediction.router)
app.include_router(uploads.router)
# app.include_router(auth.router)
app.include_router(admin.router)


Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "EDPS is live!"}
