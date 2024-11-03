import pandas as pd
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Define data for high-risk student samples
data = {
    "Age at enrollment": [27, 28, 26, 29, 30],
    "Curricular units 1st sem (credited)": [5, 5, 5, 5, 5],
    "Curricular units 1st sem (enrolled)": [5, 5, 5, 5, 5],
    "Curricular units 1st sem (evaluations)": [5, 5, 5, 5, 5],
    "Curricular units 1st sem (approved)": [1, 2, 1, 0, 2],
    "Curricular units 1st sem (grade)": [5.0, 6.0, 4.5, 4.0, 5.5],
    "Curricular units 1st sem (without evaluations)": [1, 1, 2, 1, 1],
    "Curricular units 2nd sem (credited)": [5, 5, 5, 5, 5],
    "Curricular units 2nd sem (enrolled)": [5, 5, 5, 5, 5],
    "Curricular units 2nd sem (evaluations)": [5, 5, 5, 5, 5],
    "Curricular units 2nd sem (approved)": [1, 1, 2, 1, 0],
    "Curricular units 2nd sem (grade)": [4.0, 5.5, 4.5, 3.0, 5.0],
    "Curricular units 2nd sem (without evaluations)": [1, 1, 1, 2, 1],
    "Gender_Female": [0, 1, 0, 1, 0],
    "Gender_Male": [1, 0, 1, 0, 1],
    "Tuition fees up to date_0.39316682549746695": [0, 0, 0, 0, 0],
    "Scholarship holder_1.657145144807706": [0, 0, 0, 0, 0]
}

# Create a DataFrame
high_risk_students_df = pd.DataFrame(data)

data_file_path = os.path.join(base_dir, 'data', 'high_risk_student_samples.csv')

# Save as CSV
high_risk_students_df.to_csv(data_file_path, index=False)
