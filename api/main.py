# api/main.py

from fastapi import FastAPI
from api.routes import students, predictions, uploads, admin, auth
from db.database import engine
from db.models import Base

app = FastAPI()

app.include_router(students.router)
app.include_router(predictions.router)
# app.include_router(uploads.router)
# app.include_router(auth.router)
app.include_router(admin.router)


Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "EDPS is live!"}
