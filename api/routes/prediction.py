# api/routes/prediction.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import pandas as pd
import io
from fastapi.responses import StreamingResponse

from db.models import Student, RiskPrediction
from db.database import SessionLocal
from api.schemas import StudentCreate, StudentUpdate, RiskPredictionSchema
from models.utils.system.prediction import predict_student

router = APIRouter()

# --- Utilities ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_risk_level(score: float) -> str:
    if score <= 0.4:
        return "low"
    elif score <= 0.7:
        return "moderate"
    else:
        return "high"

def predict_and_save(student, db, force_update=False):
    """
    Predict and either create or update RiskPrediction for a student.
    """
    student_dict = student.__dict__.copy()
    student_dict.pop("_sa_instance_state", None)

    raw_score, phase = predict_student(student_dict, return_phase=True)
    risk_score = 1 - raw_score
    risk_level = get_risk_level(risk_score)

    existing = db.query(RiskPrediction).filter(
        RiskPrediction.student_number == student.student_number,
        RiskPrediction.model_phase == phase
    ).first()

    if existing and not force_update:
        return None  # Skip (already exists)
    
    if existing and force_update:
        existing.risk_score = risk_score
        existing.risk_level = risk_level
        existing.timestamp = datetime.now()
        return RiskPredictionSchema.model_validate(existing)

    # Create new prediction
    new_pred = RiskPrediction(
        student_number=student.student_number,
        risk_score=risk_score,
        risk_level=risk_level,
        model_phase=phase,
        timestamp=datetime.now()
    )
    db.add(new_pred)
    return RiskPredictionSchema.model_validate(new_pred)

# --- Endpoints ---

@router.get("/predict/all")
def bulk_predict_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    predictions = []
    skipped = []

    for student in students:
        try:
            result = predict_and_save(student, db, force_update=False)
            if result:
                predictions.append(result)
            else:
                skipped.append({"student_number": student.student_number, "note": "Prediction already exists"})
        except ValueError as e:
            skipped.append({"student_number": student.student_number, "error": str(e)})

    db.commit()
    return {"predictions": predictions, "skipped": skipped}

@router.get("/predict/recalculate-all")
def recalculate_all_predictions(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    updated = []
    skipped = []

    for student in students:
        try:
            result = predict_and_save(student, db, force_update=True)
            if result:
                updated.append(result)
        except ValueError as e:
            skipped.append({"student_number": student.student_number, "error": str(e)})

    db.commit()
    return {"predictions_updated_or_created": updated, "skipped": skipped}

@router.get("/predict/by-number/{student_number}")
def predict_by_student_number(student_number: str, recalculate: bool = Query(default=False), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        result = predict_and_save(student, db, force_update=recalculate)
        db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/predictions")
def get_all_predictions(db: Session = Depends(get_db)):
    predictions = db.query(RiskPrediction).order_by(RiskPrediction.timestamp.desc()).all()
    return [RiskPredictionSchema.model_validate(p) for p in predictions]

@router.get("/predictions/{student_number}", response_model=List[RiskPredictionSchema])
def get_predictions_for_student(student_number: str, db: Session = Depends(get_db)):
    predictions = db.query(RiskPrediction).filter(
        RiskPrediction.student_number == student_number
    ).order_by(RiskPrediction.timestamp.asc()).all()

    if not predictions:
        raise HTTPException(status_code=404, detail="No predictions found for this student.")
    return [RiskPredictionSchema.model_validate(p) for p in predictions]

@router.get("/download/predictions")
def download_predictions(db: Session = Depends(get_db)):
    predictions = db.query(RiskPrediction).all()
    df = pd.DataFrame([p.__dict__ for p in predictions])
    df.drop(columns=["_sa_instance_state"], errors="ignore", inplace=True)

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(stream, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=predictions.csv"
    })

@router.get("/insights/risk-increase")
def get_biggest_risk_increases(db: Session = Depends(get_db), limit: int = 5):
    from collections import defaultdict

    all_preds = db.query(RiskPrediction).order_by(
        RiskPrediction.student_number, RiskPrediction.timestamp
    ).all()

    grouped = defaultdict(list)
    for pred in all_preds:
        grouped[pred.student_number].append(pred)

    diffs = []
    for student_number, preds in grouped.items():
        if len(preds) >= 2:
            prev, latest = preds[-2], preds[-1]
            increase = latest.risk_score - prev.risk_score
            if increase > 0:
                student = db.query(Student).filter(Student.student_number == student_number).first()
                if student:
                    diffs.append({
                        "student_number": student_number,
                        "first_name": student.first_name,
                        "last_name": student.last_name,
                        "increase": round(increase, 2),
                        "previous_score": round(prev.risk_score, 2),
                        "current_score": round(latest.risk_score, 2)
                    })

    diffs.sort(key=lambda d: d["increase"], reverse=True)
    return diffs[:limit]
