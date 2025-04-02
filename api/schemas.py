from pydantic import BaseModel
from typing import Optional

class StudentCreate(BaseModel):
    age_at_enrollment: int
    application_order: int
    curricular_units_1st_sem_enrolled: int
    daytime_evening_attendance: int
    debtor: int
    displaced: int
    gender: int
    marital_status: int
    scholarship_holder: int
    tuition_fees_up_to_date: int

class StudentUpdate(BaseModel):
    curricular_units_1st_sem_approved: Optional[int]
    curricular_units_1st_sem_grade: Optional[float]
    curricular_units_2nd_sem_grade: Optional[float]
