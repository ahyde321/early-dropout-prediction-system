import pandas as pd
import random
import os

base_dir = os.path.abspath(os.path.dirname(__file__))

high_risk_data = []
low_risk_data = []

file1_path = os.path.join(base_dir, 'high_risk_student_dataset.csv')
file2_path = os.path.join(base_dir, 'low_risk_student_dataset.csv')

# Generate 5 records likely to drop out
for _ in range(5):
    high_risk_data.append({
        'Marital status': random.choice([1, 2, 3]),
        'Application mode': random.randint(1, 10),
        'Application order': random.randint(1, 5),
        'Course': random.randint(1, 100),
        'Daytime/evening attendance': random.choice([0, 1]),
        'Previous qualification': random.randint(1, 5),  # Lower qualification level
        'Nationality': random.randint(1, 20),
        "Mother's qualification": random.randint(1, 5),  # Lower parental education
        "Father's qualification": random.randint(1, 5),
        "Mother's occupation": random.randint(1, 5),
        "Father's occupation": random.randint(1, 5),
        'Displaced': 1,  # Displacement is a risk factor
        'Educational special needs': random.choice([0, 1]),
        'Debtor': 1,  # Likely to have debts
        'Tuition fees up to date': 0,  # Fees not up to date
        'Gender': random.choice([0, 1]),
        'Scholarship holder': 0,  # Not a scholarship holder
        'Age at enrollment': random.randint(18, 25),
        'International': random.choice([0, 1]),
        'Curricular units 1st sem (credited)': random.randint(0, 3),
        'Curricular units 1st sem (enrolled)': random.randint(0, 5),
        'Curricular units 1st sem (evaluations)': random.randint(0, 5),
        'Curricular units 1st sem (approved)': random.randint(0, 2),
        'Curricular units 1st sem (grade)': random.uniform(0, 10),  # Lower grades
        'Curricular units 1st sem (without evaluations)': random.randint(1, 3),
        'Curricular units 2nd sem (credited)': random.randint(0, 3),
        'Curricular units 2nd sem (enrolled)': random.randint(0, 5),
        'Curricular units 2nd sem (evaluations)': random.randint(0, 5),
        'Curricular units 2nd sem (approved)': random.randint(0, 2),
        'Curricular units 2nd sem (grade)': random.uniform(0, 10),  # Lower grades
        'Curricular units 2nd sem (without evaluations)': random.randint(1, 3),
        'Unemployment rate': random.uniform(10, 20),
        'Inflation rate': random.uniform(3, 5),
        'GDP': random.uniform(0, 2)  # Lower GDP regions
    })

for _ in range(5):
    low_risk_data.append({
        'Marital status': random.choice([1, 2]),  # Stable marital status
        'Application mode': random.randint(1, 3),  # Preferred application modes
        'Application order': 1,  # First-choice application
        'Course': random.randint(1, 50),  # Courses with lower dropout rates
        'Daytime/evening attendance': 1,  # Daytime attendance
        'Previous qualification': random.randint(7, 10),  # High prior qualifications
        'Nationality': random.randint(1, 15),  # Stable nationalities
        "Mother's qualification": random.randint(8, 10),  # High parental education
        "Father's qualification": random.randint(8, 10),
        "Mother's occupation": random.randint(8, 10),  # Stable occupations
        "Father's occupation": random.randint(8, 10),
        'Displaced': 0,  # Not displaced
        'Educational special needs': 0,  # No special needs
        'Debtor': 0,  # No debts
        'Tuition fees up to date': 1,  # Fees paid
        'Gender': random.choice([0, 1]),
        'Scholarship holder': 1,  # Scholarship holder
        'Age at enrollment': random.randint(18, 21),  # Younger students tend to graduate more often
        'International': 0,  # Domestic students
        'Curricular units 1st sem (credited)': random.randint(5, 6),  # Full credit load
        'Curricular units 1st sem (enrolled)': random.randint(5, 6),
        'Curricular units 1st sem (evaluations)': random.randint(5, 6),
        'Curricular units 1st sem (approved)': random.randint(5, 6),
        'Curricular units 1st sem (grade)': random.uniform(16, 20),  # High grades
        'Curricular units 1st sem (without evaluations)': 0,
        'Curricular units 2nd sem (credited)': random.randint(5, 6),
        'Curricular units 2nd sem (enrolled)': random.randint(5, 6),
        'Curricular units 2nd sem (evaluations)': random.randint(5, 6),
        'Curricular units 2nd sem (approved)': random.randint(5, 6),
        'Curricular units 2nd sem (grade)': random.uniform(16, 20),  # High grades
        'Curricular units 2nd sem (without evaluations)': 0,
        'Unemployment rate': random.uniform(2, 5),  # Low unemployment
        'Inflation rate': random.uniform(0, 1),  # Low inflation
        'GDP': random.uniform(4, 6)  # High GDP regions
    })


high_risk_df = pd.DataFrame(high_risk_data)
low_risk_df = pd.DataFrame(low_risk_data)

high_risk_df.to_csv(file1_path, index=False)
low_risk_df.to_csv(file2_path, index=False)

print(f"Generated high-risk records saved to {file1_path}")
print(f"Generated low-risk records saved to {file2_path}")
