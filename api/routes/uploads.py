from fastapi import UploadFile, File, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models import Student, Notification, User
from db.database import SessionLocal
import pandas as pd
from io import StringIO
from datetime import datetime

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/grades")
def upload_grades(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = file.file.read().decode("utf-8")
    df = pd.read_csv(StringIO(contents))

    updated = []
    skipped = []

    for _, row in df.iterrows():
        student_number = row.get("student_number")
        student = db.query(Student).filter(Student.student_number == student_number).first()

        if not student:
            skipped.append(student_number)
            continue

        was_updated = False
        for field in ["curricular_units_1st_sem_approved", "curricular_units_1st_sem_grade", "curricular_units_2nd_sem_grade"]:
            if field in row and pd.notnull(row[field]):
                new_val = row[field]
                current_val = getattr(student, field)

                if pd.isna(current_val) or current_val != new_val:
                    setattr(student, field, new_val)
                    was_updated = True

        if was_updated:
            updated.append(student_number)
        else:
            skipped.append(student_number)

    db.commit()

    # Send summary notification
    recipients = db.query(User).filter(User.role.in_(["admin", "advisor"]), User.is_active == True).all()
    message = f"Grades updated for {len(updated)} students. {len(skipped)} were skipped."
    for user in recipients:
        db.add(Notification(
            user_id=user.id,
            title="Grade Upload Summary",
            message=message,
            type="info",
            read=False,
            created_at=datetime.utcnow()
        ))
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

            for field in REQUIRED_COLUMNS:
                if not student_data.get(field):
                    raise ValueError(f"Missing value for required field '{field}'")

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

    # Send summary notification
    recipients = db.query(User).filter(User.role.in_(["admin", "advisor"]), User.is_active == True).all()
    message = f"Students added: {len(success)}. Skipped: {len(skipped)}. Failed: {len(failed)}."
    for user in recipients:
        db.add(Notification(
            user_id=user.id,
            title="Student Upload Summary",
            message=message,
            type="info",
            read=False,
            created_at=datetime.utcnow()
        ))
    db.commit()

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
