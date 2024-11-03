import pandas as pd
import os

# This script will generate a csv file of high risk students
# The data below suggests all students have a high age at enrollment, low academic performance, financial
# instability, low completion and low engagement

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define data for high-risk student samples
data = {
    "Age at enrollment": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
    "Curricular units 1st sem (credited)": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Curricular units 1st sem (enrolled)": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Curricular units 1st sem (evaluations)": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Curricular units 1st sem (approved)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Curricular units 1st sem (grade)": [1.0, 1.5, 2.0, 1.0, 1.5, 2.0, 1.0, 1.5, 2.0, 1.0],
    "Curricular units 1st sem (without evaluations)": [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    "Curricular units 2nd sem (credited)": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Curricular units 2nd sem (enrolled)": [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "Curricular units 2nd sem (evaluations)": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Curricular units 2nd sem (approved)": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Curricular units 2nd sem (grade)": [1.0, 1.5, 2.0, 1.0, 1.5, 2.0, 1.0, 1.5, 2.0, 1.0],
    "Curricular units 2nd sem (without evaluations)": [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    "Gender_Female": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    "Gender_Male": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    "Tuition fees up to date_0.39316682549746695": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "Scholarship holder_1.657145144807706": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}

# Create a DataFrame
high_risk_students_df = pd.DataFrame(data)

data_file_path = os.path.join(base_dir, 'data', 'high_risk_student_samples.csv')

# Save as CSV
high_risk_students_df.to_csv(data_file_path, index=False)
