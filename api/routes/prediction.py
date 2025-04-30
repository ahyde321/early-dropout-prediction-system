# api/routes/prediction.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import pandas as pd
import io
from fastapi.responses import StreamingResponse

from db.models import Student, RiskPrediction, Notification, User
from db.database import SessionLocal
from api.schemas import StudentCreate, StudentUpdate, RiskPredictionSchema
from models.utils.system.prediction import predict_student
from models.utils.system.shap_explainer import explain_student

router = APIRouter()

# --- Utilities ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_risk_level(score: float) -> str:
    if score <= 0.5:
        return "low"
    elif score <= 0.75:
        return "moderate"
    else:
        return "high"

def predict_and_save(student, db, force_update=False, notify=True):
    student_dict = student.__dict__.copy()
    student_dict.pop("_sa_instance_state", None)

    raw_score, phase = predict_student(student_dict, return_phase=True)
    risk_score = 1 - raw_score
    risk_level = get_risk_level(risk_score)

    shap_explanation = explain_student(student_dict)

    existing = db.query(RiskPrediction).filter(
        RiskPrediction.student_number == student.student_number,
        RiskPrediction.model_phase == phase
    ).first()

    if existing and not force_update:
        return None

    if existing and force_update:
        existing.risk_score = risk_score
        existing.risk_level = risk_level
        existing.timestamp = datetime.now()
        existing.shap_values = shap_explanation
        return RiskPredictionSchema.model_validate(existing)

    new_pred = RiskPrediction(
        student_number=student.student_number,
        risk_score=risk_score,
        risk_level=risk_level,
        model_phase=phase,
        timestamp=datetime.now(),
        shap_values=shap_explanation
    )
    db.add(new_pred)

    # Send notification only if not in bulk mode
    if notify and risk_level in ["moderate", "high"]:
        advisors = db.query(User).filter(User.role == "advisor", User.is_active == True).all()
        for advisor in advisors:
            db.add(Notification(
                user_id=advisor.id,
                title="Risk Prediction Alert",
                message=f"{student.first_name} {student.last_name} predicted as {risk_level.upper()} risk.",
                type="alert" if risk_level == "high" else "info",
                student_number=student.student_number,
                read=False,
                created_at=datetime.utcnow()
            ))

    return RiskPredictionSchema.model_validate(new_pred)

# --- Endpoints ---

@router.get("/predict/all")
def bulk_predict_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    predictions = []
    skipped = []
    risk_summary = {"high": 0, "moderate": 0, "low": 0}
    last_phase = ""

    for student in students:
        try:
            result = predict_and_save(student, db, force_update=False, notify=False)
            if result:
                predictions.append(result)
                risk_summary[result.risk_level] += 1
                last_phase = result.model_phase
            else:
                skipped.append({"student_number": student.student_number, "note": "Prediction already exists"})
        except ValueError as e:
            skipped.append({"student_number": student.student_number, "error": str(e)})

    db.commit()

    recipients = db.query(User).filter(User.role.in_(["advisor", "admin"]), User.is_active == True).all()
    if predictions:
        message = f"{len(predictions)} predictions run (Phase: {last_phase}). High: {risk_summary['high']}, Moderate: {risk_summary['moderate']}, Low: {risk_summary['low']}"
        for advisor in recipients:
            db.add(Notification(
                user_id=advisor.id,
                title="Bulk Risk Prediction Summary",
                message=message,
                type="info",
                read=False,
                created_at=datetime.utcnow()
            ))
        db.commit()

    return {"predictions": predictions, "skipped": skipped}

@router.get("/predict/recalculate-all")
def recalculate_all_predictions(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    updated = []
    skipped = []
    risk_summary = {"high": 0, "moderate": 0, "low": 0}
    last_phase = ""

    for student in students:
        try:
            result = predict_and_save(student, db, force_update=True, notify=False)
            if result:
                updated.append(result)
                risk_summary[result.risk_level] += 1
                last_phase = result.model_phase
        except ValueError as e:
            skipped.append({"student_number": student.student_number, "error": str(e)})

    db.commit()

    advisors = db.query(User).filter(User.role == "advisor", User.is_active == True).all()
    if updated:
        message = f"{len(updated)} recalculated predictions (Phase: {last_phase}). High: {risk_summary['high']}, Moderate: {risk_summary['moderate']}, Low: {risk_summary['low']}"
        for advisor in advisors:
            db.add(Notification(
                user_id=advisor.id,
                title="Recalculated Risk Predictions",
                message=message,
                type="info",
                read=False,
                created_at=datetime.utcnow()
            ))
        db.commit()

    return {"predictions_updated_or_created": updated, "skipped": skipped}

@router.get("/predict/by-number/{student_number}")
def predict_by_student_number(student_number: str, recalculate: bool = Query(default=False), db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    try:
        result = predict_and_save(student, db, force_update=recalculate, notify=True)
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