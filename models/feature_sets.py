EARLY_FIELDS = [
    "student_number", "first_name", "last_name","age_at_enrollment", "application_order", "curricular_units_1st_sem_enrolled",
    "daytime_evening_attendance", "debtor", "displaced", "gender",
    "marital_status", "scholarship_holder", "tuition_fees_up_to_date"
]

MID_FIELDS = EARLY_FIELDS[:1] + [  # starts with shared fields
    "curricular_units_1st_sem_approved",
    "curricular_units_1st_sem_grade"
]

FINAL_FIELDS = MID_FIELDS + [
    "curricular_units_2nd_sem_grade"
]
