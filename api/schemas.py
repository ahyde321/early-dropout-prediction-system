from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime

# ===============================
# 🌱 STUDENT SCHEMAS
# ===============================

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


class StudentSchema(StudentCreate, StudentUpdate):
    model_config = ConfigDict(from_attributes=True)


# ===============================
# 🔐 AUTH / USER SCHEMAS
# ===============================

class Token(BaseModel):
    access_token: str
    token_type: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must include at least one number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must include at least one uppercase letter")
        return v


class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class RoleUpdateRequest(BaseModel):
    user_id: int
    role: str


class UserUpdateRequest(BaseModel):
    user_id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


# ===============================
# 📊 RISK PREDICTION SCHEMA
# ===============================

class RiskPredictionSchema(BaseModel):
    student_number: str
    risk_score: float
    risk_level: str
    model_phase: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
