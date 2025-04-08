from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from typing import List

class StudentCreate(BaseModel):
    student_number: str
    first_name: str
    last_name: str
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

    model_config = ConfigDict(from_attributes=True)


class StudentUpdate(BaseModel):
    curricular_units_1st_sem_approved: Optional[int] = None
    curricular_units_1st_sem_grade: Optional[float] = None
    curricular_units_2nd_sem_grade: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class RiskPredictionSchema(BaseModel):
    student_number: str
    risk_score: float
    risk_level: str
    model_phase: str
    timestamp: datetime  # formatted string

    model_config = {
        "from_attributes": True
    }

class StudentSchema(BaseModel):
    student_number: str
    first_name: str
    last_name: str
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
    curricular_units_1st_sem_approved: Optional[int] = None
    curricular_units_1st_sem_grade: Optional[float] = None
    curricular_units_2nd_sem_grade: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
