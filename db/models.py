from sqlalchemy import Column, Integer, Float, Boolean, String
from db.database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    age_at_enrollment = Column(Integer)
    application_order = Column(Integer)
    curricular_units_1st_sem_enrolled = Column(Integer)
    daytime_evening_attendance = Column(Integer)
    debtor = Column(Integer)
    displaced = Column(Integer)
    gender = Column(Integer)
    marital_status = Column(Integer)
    scholarship_holder = Column(Integer)
    tuition_fees_up_to_date = Column(Integer)

    # Mid/Final data (nullable)
    curricular_units_1st_sem_approved = Column(Integer, nullable=True)
    curricular_units_1st_sem_grade = Column(Float, nullable=True)
    curricular_units_2nd_sem_grade = Column(Float, nullable=True)