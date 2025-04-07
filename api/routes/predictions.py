# api/routes/students.py

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

@router.get("/predict/by-number/{student_number}")
def predict_by_student_number(student_number: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_dict = student.__dict__.copy()
    student_dict.pop("_sa_instance_state", None)

    try:
        risk_score = predict_student(student_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "student_number": student_number,
        "risk_score": round(risk_score, 3),
        "risk_level": get_risk_level(risk_score)
    }


