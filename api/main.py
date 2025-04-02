from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db.models import Student
from api.schemas import StudentCreate, StudentUpdate
from typing import List
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def root():
    return {"message": "EDPS is live!"}

# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/students/")
def create_student(data: StudentCreate, db: Session = Depends(get_db)):
    student = Student(**data.dict())
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(404, detail="Student not found")
    return student

@app.patch("/students/{student_id}")
def update_student(student_id: int, updates: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(Student).get(student_id)
    if not student:
        raise HTTPException(404, detail="Student not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(student, key, value)
    db.commit()
    return {"message": "Student updated"}
