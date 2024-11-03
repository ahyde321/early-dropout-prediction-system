import pandas as pd
import os

# This script will generate a csv file of high risk students
# The data below suggests all students have a low age at enrollment, good academic performance, financial
# stability, good completion and good engagement

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define data for low-risk student samples
low_risk_data = {
    "Age at enrollment": [19, 20, 21, 22, 23],
    "Curricular units 1st sem (credited)": [5, 5, 5, 5, 5],
    "Curricular units 1st sem (enrolled)": [5, 5, 5, 5, 5],
    "Curricular units 1st sem (evaluations)": [5, 5, 5, 5, 5],
    "Curricular units 1st sem (approved)": [5, 5, 5, 4, 5],
    "Curricular units 1st sem (grade)": [14.0, 15.0, 13.5, 14.5, 16.0],
    "Curricular units 1st sem (without evaluations)": [0, 0, 0, 0, 0],
    "Curricular units 2nd sem (credited)": [5, 5, 5, 5, 5],
    "Curricular units 2nd sem (enrolled)": [5, 5, 5, 5, 5],
    "Curricular units 2nd sem (evaluations)": [5, 5, 5, 5, 5],
    "Curricular units 2nd sem (approved)": [5, 5, 5, 5, 4],
    "Curricular units 2nd sem (grade)": [15.0, 14.5, 16.0, 15.5, 14.0],
    "Curricular units 2nd sem (without evaluations)": [0, 0, 0, 0, 0],
    "Gender_Female": [1, 0, 1, 0, 1],
    "Gender_Male": [0, 1, 0, 1, 0],
    "Tuition fees up to date_0.39316682549746695": [1, 1, 1, 1, 1],
    "Scholarship holder_1.657145144807706": [1, 1, 1, 0, 1]
}

# Create a DataFrame
low_risk_students_df = pd.DataFrame(low_risk_data)
data_file_path = os.path.join(base_dir, 'data', 'low_risk_student_samples.csv')

# Save as CSV
low_risk_students_df.to_csv(data_file_path, index=False)
