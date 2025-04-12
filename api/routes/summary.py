from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.models import Student, RiskPrediction
from db.database import SessionLocal

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/students/summary")
def get_risk_summary(db: Session = Depends(get_db)):
    from db.models import RiskPrediction

    # Group latest predictions
    students = db.query(Student).all()
    current_counts = {"high": 0, "moderate": 0, "low": 0}
    previous_counts = {"high": 0, "moderate": 0, "low": 0}

    for s in students:
        preds = (
            db.query(RiskPrediction)
            .filter(RiskPrediction.student_number == s.student_number)
            .order_by(RiskPrediction.timestamp.desc())
            .limit(2)
            .all()
        )

        if len(preds) > 0:
            current_counts[preds[0].risk_level] += 1
        if len(preds) > 1:
            previous_counts[preds[1].risk_level] += 1

    # Build result with trends
    result = {}
    for level in current_counts.keys():
        result[level] = {
            "count": current_counts[level],
            "trend": current_counts[level] - previous_counts[level]
        }

    return result


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

    query = db.query(RiskPrediction).join(RiskPrediction.student)

    if filter_field and filter_value is not None:
        if filter_field in valid_fields:
            field = valid_fields[filter_field]
            query = query.filter(field == int(filter_value))
        else:
            return {"error": f"Invalid filter field: {filter_field}"}

    latest_preds = (
        query.order_by(RiskPrediction.timestamp.desc())
        .distinct(RiskPrediction.student_number, RiskPrediction.model_phase)
        .all()
    )

    for pred in latest_preds:
        if pred.model_phase in phase_levels and pred.risk_level in risk_levels:
            result[pred.model_phase][pred.risk_level] += 1

    return result
