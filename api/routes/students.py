# api/routes/students.py

from fastapi import UploadFile, File, APIRouter, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from db.models import Student
from db.database import SessionLocal
from api.schemas import StudentCreate, StudentUpdate, StudentSchema
from models.utils.system.prediction import predict_student
from typing import List
from fastapi.responses import StreamingResponse

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/students/create")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**student.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


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
        raise HTTPException(404, detail="Student not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return {"message": "Student updated", "student": student.id}

@router.get("/students/list")
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [
        {
            "student_number": s.student_number,
            "first_name": s.first_name,
            "last_name": s.last_name
        }
        for s in students
    ]

@router.post("/students/bulk-upload-file")
async def bulk_upload_students(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(e)}")

    success = []
    failed = []

    for i, row in df.iterrows():
        try:
            student_data = row.to_dict()
            student = Student(**student_data)
            db.add(student)
            success.append(student_data)
        except Exception as e:
            failed.append({"row": i, "error": str(e)})

    db.commit()
    return {
        "added": len(success),
        "failed": len(failed),
        "details": {"failures": failed}
    }

from fastapi.responses import StreamingResponse
import io

@router.get("/download/students")
def download_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    df = pd.DataFrame([s.__dict__ for s in students])
    df = df.drop(columns=["_sa_instance_state"], errors="ignore")

    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)

    return StreamingResponse(stream, media_type="text/csv", headers={
        "Content-Disposition": "attachment; filename=students.csv"
    })

@router.get("/students/{student_number}/status")
def get_student_status(student_number: str, db: Session = Depends(get_db)):
    from db.models import Student, RiskPrediction
    from api.schemas import StudentSchema, RiskPredictionSchema

    student = db.query(Student).filter(Student.student_number == student_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get the latest prediction (if any), by timestamp
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
    from db.models import Student, RiskPrediction
    from api.schemas import StudentSchema, RiskPredictionSchema

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

