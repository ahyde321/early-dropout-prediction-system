# api/routes/students.py

from fastapi import UploadFile, File, APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import io

from db.models import Student, RiskPrediction
from db.database import SessionLocal
from api.schemas import StudentCreate, StudentUpdate, StudentSchema, RiskPredictionSchema
from models.utils.system.prediction import predict_student

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === STUDENT ROUTES ===

@router.post("/students/create", response_model=StudentSchema)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    student_model = Student(**student.model_dump())
    db.add(student_model)
    db.commit()
    db.refresh(student_model)
    return student_model

@router.get("/students/by-number/{student_number}", response_model=StudentSchema)
def get_student_by_number(student_number: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.patch("/students/{student_id}")
def update_student(student_id: int, updates: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return {"message": "Student updated", "student": student.id}

@router.get("/students/list")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    results = []

    for s in students:
        predictions = (
            db.query(RiskPrediction)
            .filter(RiskPrediction.student_number == s.student_number)
            .order_by(RiskPrediction.timestamp.desc())
            .limit(2)
            .all()
        )

        latest = predictions[0] if predictions else None
        previous = predictions[1] if len(predictions) > 1 else None

        risk_trend = None
        if latest and previous:
            symbol = "↑" if latest.risk_level > previous.risk_level else ("↓" if latest.risk_level < previous.risk_level else "→")
            risk_trend = {
                "previous": previous.risk_level,
                "current": latest.risk_level,
                "change": symbol
            }

        results.append({
            "student_number": s.student_number,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "risk_level": latest.risk_level if latest else None,
            "risk_score": latest.risk_score if latest else None,
            "risk_trend": risk_trend
        })
        print("📦 student:", {
            "student_number": s.student_number,
            "risk_score": latest.risk_score if latest else None
        })

    return results

@router.get("/download/students")
def download_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    df = pd.DataFrame([s.__dict__ for s in students])
    df.drop(columns=["_sa_instance_state"], errors="ignore", inplace=True)

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(stream, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=students.csv"
    })

@router.get("/students/{student_number}/status")
def get_student_status(student_number: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    latest_prediction = (
        db.query(RiskPrediction)
        .filter(RiskPrediction.student_number == student_number)
        .order_by(RiskPrediction.timestamp.desc())
        .first()
    )

    return {
        "student": StudentSchema.model_validate(student),
        "latest_prediction": RiskPredictionSchema.model_validate(latest_prediction) if latest_prediction else None
    }

@router.get("/students/{student_number}/history")
def get_student_history(student_number: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    predictions = (
        db.query(RiskPrediction)
        .filter(RiskPrediction.student_number == student_number)
        .order_by(RiskPrediction.timestamp.asc())
        .all()
    )

    return {
        "student": StudentSchema.model_validate(student),
        "predictions": [RiskPredictionSchema.model_validate(p) for p in predictions]
    }

@router.get("/students/distinct-values")
def get_distinct_values(field: str = Query(...), db: Session = Depends(get_db)):
    from db.models import Student

    valid_fields = {
        "age_at_enrollment": Student.age_at_enrollment,
        "application_order": Student.application_order,
        "curricular_units_1st_sem_enrolled": Student.curricular_units_1st_sem_enrolled,
        "daytime_evening_attendance": Student.daytime_evening_attendance,
        "debtor": Student.debtor,
        "displaced": Student.displaced,
        "gender": Student.gender,
        "marital_status": Student.marital_status,
        "scholarship_holder": Student.scholarship_holder,
        "tuition_fees_up_to_date": Student.tuition_fees_up_to_date,
    }

    if field not in valid_fields:
            return {"error": "Invalid field"}


    column = valid_fields[field]
    distinct = db.query(column).distinct().all()
    return [d[0] for d in distinct]

@router.get("/students/with-notes")
def get_students_with_notes(db: Session = Depends(get_db)):
    students = db.query(Student).filter(Student.notes.isnot(None)).all()

    return [
        {
            "student_number": s.student_number,
            "first_name": s.first_name,
            "last_name": s.last_name,
            "reason": s.notes  # use the actual note as the "reason"
        }
        for s in students
    ]
