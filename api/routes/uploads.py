from fastapi import UploadFile, File
import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session
from db.models import Student
from db.database import SessionLocal
from fastapi import UploadFile, File, APIRouter, Depends, HTTPException

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/grades")
def upload_grades(file: UploadFile = File(...), db: Session = Depends(get_db)):
    from db.models import Student

    contents = file.file.read().decode("utf-8")
    df = pd.read_csv(StringIO(contents))

    updated = []
    skipped = []

    for _, row in df.iterrows():
        student = db.query(Student).filter(Student.student_number == row["student_number"]).first()
        if not student:
            skipped.append(row["student_number"])
            continue

        # Update only grade-related fields if provided
        for field in ["curricular_units_1st_sem_approved", "curricular_units_1st_sem_grade", "curricular_units_2nd_sem_grade"]:
            if field in row and pd.notnull(row[field]):
                setattr(student, field, row[field])

        updated.append(student.student_number)

    db.commit()

    return {
        "students_updated": updated,
        "students_skipped": skipped
    }

@router.post("/upload/students")
async def bulk_upload_students(file: UploadFile = File(...), db: Session = Depends(get_db)):
    MAX_SIZE_MB = 2
    REQUIRED_COLUMNS = {"student_number", "first_name", "last_name"}

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    if len(content) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File too large. Limit is {MAX_SIZE_MB}MB.")

    try:
        df = pd.read_csv(StringIO(content.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read CSV: {str(e)}")

    missing_cols = REQUIRED_COLUMNS - set(df.columns)
    if missing_cols:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing_cols)}"
        )

    success = []
    skipped = []
    failed = []

    for i, row in df.iterrows():
        try:
            student_data = row.to_dict()
            student_number = student_data.get("student_number")

            # Check required values
            for field in REQUIRED_COLUMNS:
                if not student_data.get(field):
                    raise ValueError(f"Missing value for required field '{field}'")

            # Check for duplicate
            existing = db.query(Student).filter(Student.student_number == student_number).first()
            if existing:
                skipped.append({
                    "row": i + 1,
                    "student_number": student_number,
                    "reason": "Duplicate student_number"
                })
                continue

            student = Student(**student_data)
            db.add(student)
            success.append(student_data)

        except Exception as e:
            failed.append({
                "row": i + 1,
                "student_number": row.get("student_number"),
                "error": str(e)
            })

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database commit failed: {str(e)}")

    return {
        "message": "Upload completed",
        "added": len(success),
        "skipped": len(skipped),
        "failed": len(failed),
        "details": {
            "skipped": skipped,
            "failures": failed
        }
    }
