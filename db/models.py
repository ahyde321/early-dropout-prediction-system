from sqlalchemy import Column, Integer, Float, Boolean, String
from db.database import Base

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

    # Mid/Final data (nullable)
    curricular_units_1st_sem_approved = Column(Integer, nullable=True)
    curricular_units_1st_sem_grade = Column(Float, nullable=True)
    curricular_units_2nd_sem_grade = Column(Float, nullable=True)