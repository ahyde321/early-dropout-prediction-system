import pandas as pd
import joblib
import os
from 

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load the trained model, scalers, and feature names
model = joblib.load(os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib'))
scaler = joblib.load(os.path.join(base_dir, 'models', 'scaler.joblib'))
min_max_scaler = joblib.load(os.path.join(base_dir, 'models', 'min_max_scaler.joblib'))
feature_names = joblib.load(os.path.join(base_dir, 'models', 'feature_names.joblib'))
numerical_columns = joblib.load(os.path.join(base_dir, 'models', 'numerical_columns.joblib'))

sample = pd.read_csv(os.path.join(base_dir, 'data', 'high_risk_student_samples.csv'))

print("Original data for each student:")
for idx, row in sample.iterrows():
    print(f"\nStudent {idx + 1}:")
    for column in sample.columns:
        print(f"{column}: {row[column]}")

prep

# Make predictions for all students
predictions = model.predict(sample)

# Output the predictions for each student
print("\nPredictions for each student (0 = Graduate, 1 = Dropout):")
for idx, prediction in enumerate(predictions):
    print(f"Student {idx + 1}: Prediction = {prediction}")
