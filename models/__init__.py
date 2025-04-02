from pydantic import BaseModel

# EARLY MODEL INPUT
class EarlyStudentData(BaseModel):
    age_at_enrollment: int
    application_order: int
    curricular_units_1st_sem_enrolled: int
    daytime_evening_attendance: int  # 1 = Daytime, 0 = Evening (or however it's encoded)
    debtor: int                      # 1 = Yes, 0 = No
    displaced: int
    gender: int                      # Consider using enums if applicable
    marital_status: int
    scholarship_holder: int
    tuition_fees_up_to_date: int

# MID MODEL INPUT
class MidStudentData(BaseModel):
    age_at_enrollment: int
    curricular_units_1st_sem_approved: int
    curricular_units_1st_sem_enrolled: int
    curricular_units_1st_sem_grade: float
    debtor: int
    displaced: int
    gender: int
    marital_status: int
    scholarship_holder: int
    tuition_fees_up_to_date: int

# FINAL MODEL INPUT
class FinalStudentData(BaseModel):
    age_at_enrollment: int
    curricular_units_1st_sem_approved: int
    curricular_units_1st_sem_enrolled: int
    curricular_units_1st_sem_grade: float
    curricular_units_2nd_sem_grade: float
    debtor: int
    displaced: int
    gender: int
    scholarship_holder: int
    tuition_fees_up_to_date: int
