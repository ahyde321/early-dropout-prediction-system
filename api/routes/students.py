# api/routes/students.py

from fastapi import UploadFile, File, APIRouter, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from db.models import Student
from db.database import SessionLocal
from api.schemas import StudentCreate, StudentUpdate
from typing import List

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/students/")
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**student.model_dump())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(404, detail="Student not found")
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

@router.get("/students/")
def list_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return [s.__dict__ for s in students]

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

@router.delete("/dev/wipe-students")
def wipe_students(db: Session = Depends(get_db)):
    db.query(Student).delete()
    db.commit()
    return {"message": "All student records deleted"}
