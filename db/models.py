from sqlalchemy import Column, Integer, Float, Boolean, String, ForeignKey, DateTime, UniqueConstraint
from datetime import timezone
from db.database import Base
from sqlalchemy.orm import relationship



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
    predictions = relationship("RiskPrediction", back_populates="student", cascade="all, delete-orphan")

    # Mid/Final data (nullable)
    curricular_units_1st_sem_approved = Column(Integer, nullable=True)
    curricular_units_1st_sem_grade = Column(Float, nullable=True)
    curricular_units_2nd_sem_grade = Column(Float, nullable=True)

    
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class RiskPrediction(Base):
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String, ForeignKey("students.student_number"))
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    model_phase = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now())

    student = relationship("Student", back_populates="predictions")
    __table_args__ = (UniqueConstraint('student_number', 'model_phase', name='uq_prediction_per_phase'),)

from sqlalchemy import Column, Integer, String, Boolean
from db.database import Base

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, default="advisor")  # 'advisor', 'admin', etc.
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)



