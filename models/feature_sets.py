EARLY_FIELDS = ['student_number', 'first_name', 'last_name', 'marital_status', 'previous_qualification_grade', 'admission_grade',
                'displaced', 'debtor', 'tuition_fees_up_to_date', 'gender', 'scholarship_holder', 'age_at_enrollment',
                'curricular_units_1st_sem_enrolled']

MID_FIELDS = EARLY_FIELDS[:1] + [  # starts with shared fields
    "curricular_units_1st_sem_approved",
    "curricular_units_1st_sem_grade"
]

FINAL_FIELDS = MID_FIELDS + [
    "curricular_units_2nd_sem_grade"
]

RISK_THRESHOLDS = {
    "low": 0.4,
    "medium": 0.7
}

