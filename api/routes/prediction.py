# api/routes/prediction.py

from fastapi import UploadFile, File, APIRouter, Depends, HTTPException
import pandas as pd
import io
from sqlalchemy.orm import Session
from db.models import Student
from db.database import SessionLocal
from api.schemas import StudentCreate, StudentUpdate
from models.utils.system.prediction import predict_student
from typing import List
from models.feature_sets import get_risk_level
from fastapi.responses import StreamingResponse


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Query

from api.schemas import RiskPredictionSchema  # make sure this import is at the top

@router.get("/predict/by-number/{student_number}")
def predict_by_student_number(
    student_number: str,
    recalculate: bool = Query(default=False),
    db: Session = Depends(get_db)
):
    from models.utils.system.prediction import predict_student
    from models.feature_sets import get_risk_level
    from db.models import RiskPrediction
    from api.schemas import RiskPredictionSchema
    from datetime import datetime

    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student_dict = student.__dict__.copy()
    student_dict.pop("_sa_instance_state", None)

    try:
        risk_score, phase = predict_student(student_dict, return_phase=True)
        risk_level = get_risk_level(risk_score)

        existing = (
            db.query(RiskPrediction)
            .filter(RiskPrediction.student_number == student_number)
            .filter(RiskPrediction.model_phase == phase)
            .first()
        )

        if existing:
            if recalculate:
                existing.risk_score = risk_score
                existing.risk_level = risk_level
                existing.timestamp = datetime.now()
                db.commit()
            return RiskPredictionSchema.model_validate(existing)

        new_prediction = RiskPrediction(
            student_number=student_number,
            risk_score=risk_score,
            risk_level=risk_level,
            model_phase=phase,
            timestamp=datetime.now()
        )
        db.add(new_prediction)
        db.commit()

        return RiskPredictionSchema.model_validate(new_prediction)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/predict/all")
def bulk_predict_all_students(db: Session = Depends(get_db)):
    from models.utils.system.prediction import predict_student
    from models.feature_sets import get_risk_level
    from db.models import RiskPrediction
    from api.schemas import RiskPredictionSchema
    from datetime import datetime

    students = db.query(Student).all()
    results = []
    skipped = []

    for student in students:
        student_dict = student.__dict__.copy()
        student_dict.pop("_sa_instance_state", None)

        try:
            risk_score, new_phase = predict_student(student_dict, return_phase=True)
            risk_level = get_risk_level(risk_score)

            existing = (
                db.query(RiskPrediction)
                .filter(RiskPrediction.student_number == student.student_number)
                .filter(RiskPrediction.model_phase == new_phase)
                .first()
            )

            if existing:
                skipped.append({
                    "student_number": student.student_number,
                    "note": f"{new_phase.capitalize()} prediction already exists"
                })
                continue

            prediction = RiskPrediction(
                student_number=student.student_number,
                risk_score=risk_score,
                risk_level=risk_level,
                model_phase=new_phase,
                timestamp=datetime.now()
            )
            db.add(prediction)
            results.append(RiskPredictionSchema.model_validate(prediction))

        except ValueError as e:
            skipped.append({
                "student_number": student.student_number,
                "error": str(e)
            })

    db.commit()

    return {
        "predictions": results,
        "skipped": skipped
    }


@router.get("/predictions")
def get_all_predictions(db: Session = Depends(get_db)):
    from db.models import RiskPrediction
    from api.schemas import RiskPredictionSchema

    predictions = db.query(RiskPrediction).order_by(RiskPrediction.timestamp.desc()).all()
    return [RiskPredictionSchema.model_validate(p) for p in predictions]

@router.get("/predictions/{student_number}", response_model=List[RiskPredictionSchema])
def get_predictions_for_student(student_number: str, db: Session = Depends(get_db)):
    from db.models import RiskPrediction

    predictions = (
        db.query(RiskPrediction)
        .filter(RiskPrediction.student_number == student_number)
        .order_by(RiskPrediction.timestamp.asc())  # Optional: sort oldest → newest
        .all()
    )

    if not predictions:
        raise HTTPException(status_code=404, detail="No predictions found for this student.")

    return [RiskPredictionSchema.model_validate(p) for p in predictions]


@router.get("/download/predictions")
def download_predictions(db: Session = Depends(get_db)):
    from db.models import RiskPrediction

    predictions = db.query(RiskPrediction).all()
    df = pd.DataFrame([p.__dict__ for p in predictions])
    df = df.drop(columns=["_sa_instance_state"], errors="ignore")

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(stream, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=predictions.csv"
    })
