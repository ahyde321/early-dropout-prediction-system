# api/routes/admin.py

from fastapi import UploadFile, File, APIRouter, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from db.models import Student
from db.database import SessionLocal
from api.schemas import StudentCreate, StudentUpdate
from models.utils.system.prediction import predict_student
from typing import List

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
    from db.models import RiskPrediction
    
    # Check if there are any predictions
    prediction_count = db.query(RiskPrediction).count()
    if prediction_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot wipe students while {prediction_count} predictions exist. Please wipe predictions first."
        )
    
    db.query(Student).delete()
    db.commit()
    return {"message": "All student records deleted"}

@router.delete("/dev/wipe-predictions")
def wipe_predictions(db: Session = Depends(get_db)):
    from db.models import RiskPrediction

    deleted = db.query(RiskPrediction).delete()
    db.commit()
    return {"message": f"All {deleted} prediction records deleted"}
