# api/routes/admin.py

from fastapi import UploadFile, File, APIRouter, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from db.models import Student
from db.database import SessionLocal
from api.schemas import StudentCreate, StudentUpdate
from models.utils.system.prediction import predict_student
from typing import List
from models.feature_sets import get_risk_level

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.delete("/dev/wipe-students")
def wipe_students(db: Session = Depends(get_db)):
    db.query(Student).delete()
    db.commit()
    return {"message": "All student records deleted"}

