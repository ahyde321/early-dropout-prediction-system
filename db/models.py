from datetime import datetime
from sqlalchemy import (
    Column, Integer, Float, String, Boolean,
    ForeignKey, DateTime, UniqueConstraint
)
from sqlalchemy.orm import relationship
from db.database import Base

# === Student Model ===
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    age_at_enrollment = Column(Integer, nullable=False)
    application_order = Column(Integer, nullable=False)
    curricular_units_1st_sem_enrolled = Column(Integer, nullable=False)
    daytime_evening_attendance = Column(Integer, nullable=False)
    debtor = Column(Integer, nullable=False)
    displaced = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    marital_status = Column(Integer, nullable=False)
    scholarship_holder = Column(Integer, nullable=False)
    tuition_fees_up_to_date = Column(Integer, nullable=False)

    # Nullable mid/final academic data
    curricular_units_1st_sem_approved = Column(Integer, nullable=True)
    curricular_units_1st_sem_grade = Column(Float, nullable=True)
    curricular_units_2nd_sem_grade = Column(Float, nullable=True)

    notes = Column(String, nullable=True)


    # Relationships
    predictions = relationship(
        "RiskPrediction",
        back_populates="student",
        cascade="all, delete-orphan"
    )

# === Risk Prediction Model ===
class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String, ForeignKey("students.student_number"))
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)  # e.g. "low", "medium", "high"
    model_phase = Column(String, nullable=False)  # e.g. "early", "mid", "final"
    timestamp = Column(DateTime, default=lambda: datetime.now())

    # Relationships
    student = relationship("Student", back_populates="predictions")

    # Constraint: 1 prediction per student per model phase
    __table_args__ = (
        UniqueConstraint('student_number', 'model_phase', name='uq_prediction_per_phase'),
    )

# === User Model ===
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, default="advisor")  # 'advisor' or 'admin'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    token_version: int = Column(Integer, default=0)  # Used for stateless logout
