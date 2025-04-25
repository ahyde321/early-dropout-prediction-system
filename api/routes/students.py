from fastapi import UploadFile, File, APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, aliased
from typing import List
import pandas as pd
import io
from sqlalchemy import func

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
    valid_fields = {
        "marital_status": Student.marital_status,
        "previous_qualification_grade": Student.previous_qualification_grade,
        "admission_grade": Student.admission_grade,
        "displaced": Student.displaced,
        "debtor": Student.debtor,
        "tuition_fees_up_to_date": Student.tuition_fees_up_to_date,
        "gender": Student.gender,
        "scholarship_holder": Student.scholarship_holder,
        "age_at_enrollment": Student.age_at_enrollment,
        "curricular_units_1st_sem_enrolled": Student.curricular_units_1st_sem_enrolled,
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
            "reason": s.notes
        }
        for s in students
    ]

@router.get("/students/summary-by-phase")
def get_risk_summary_by_phase(
    filter_field: str = Query(None),
    filter_value: str = Query(None),
    db: Session = Depends(get_db)
):
    phase_levels = ["early", "mid", "final"]
    risk_levels = ["high", "moderate", "low"]
    result = {phase: {level: 0 for level in risk_levels} for phase in phase_levels}

    valid_fields = {
        "marital_status": Student.marital_status,
        "previous_qualification_grade": Student.previous_qualification_grade,
        "admission_grade": Student.admission_grade,
        "displaced": Student.displaced,
        "debtor": Student.debtor,
        "tuition_fees_up_to_date": Student.tuition_fees_up_to_date,
        "gender": Student.gender,
        "scholarship_holder": Student.scholarship_holder,
        "age_at_enrollment": Student.age_at_enrollment,
        "curricular_units_1st_sem_enrolled": Student.curricular_units_1st_sem_enrolled,
    }

    from sqlalchemy import select, desc
    from sqlalchemy.orm import aliased
    from sqlalchemy.sql import func, literal_column
    from sqlalchemy import distinct
    from sqlalchemy.sql import label
    from sqlalchemy import over

    latest_pred_subquery = (
        db.query(
            RiskPrediction.id,
            RiskPrediction.student_number,
            RiskPrediction.model_phase,
            RiskPrediction.risk_level,
            RiskPrediction.timestamp,
            func.row_number().over(
                partition_by=(RiskPrediction.student_number, RiskPrediction.model_phase),
                order_by=RiskPrediction.timestamp.desc()
            ).label("rn")
        )
    )

    if filter_field and filter_value is not None:
        if filter_field in valid_fields:
            student_subq = db.query(Student.student_number).filter(valid_fields[filter_field] == filter_value).subquery()
            latest_pred_subquery = latest_pred_subquery.filter(RiskPrediction.student_number.in_(select(student_subq)))
        else:
            return {"error": f"Invalid filter field: {filter_field}"}

    latest_pred_subquery = latest_pred_subquery.subquery()
    alias_pred = aliased(RiskPrediction, latest_pred_subquery)

    latest_preds = db.query(alias_pred).filter(latest_pred_subquery.c.rn == 1).all()

    for pred in latest_preds:
        if pred.model_phase in phase_levels and pred.risk_level in risk_levels:
            result[pred.model_phase][pred.risk_level] += 1

    return result
