import sys
import os
import pandas as pd
import joblib

# Dynamically add the project root to sys.path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

# Import the preprocessing function
from pipeline.preprocess_student_dropout_data import preprocess_student_dropout_data

# Define the paths
input_file = os.path.join(base_dir, 'data', 'raw', 'low_risk_student_dataset.csv')
preprocessed_output_file = os.path.join(base_dir, 'data', 'test', 'preprocessed_low_risk_students.csv')
model_file = os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib')
feature_names_file = os.path.join(base_dir, 'models', 'feature_names.joblib')

# Load the trained model and feature names
model = joblib.load(model_file)
feature_names = joblib.load(feature_names_file)

# Preprocess the data
print("Preprocessing data...")
preprocess_student_dropout_data(
    input_file=input_file,
    output_file=preprocessed_output_file,
)

# Load the preprocessed data
preprocessed_data = pd.read_csv(preprocessed_output_file)

# Align features with the model
print("Aligning features with the model...")
missing_features = []
for feature in feature_names:
    if feature not in preprocessed_data.columns:
        preprocessed_data[feature] = 0  # Add missing features with a default value
        missing_features.append(feature)

if missing_features:
    print(f"Warning: Missing features in data: {missing_features}")

# Ensure the columns are in the same order as during training
preprocessed_data = preprocessed_data[feature_names]

# Make predictions
print("Making predictions...")
predictions = model.predict(preprocessed_data)

# Output predictions
print("\nPredictions for each student (0 = Graduate, 1 = Dropout):")
for idx, prediction in enumerate(predictions):
    label = "Graduate" if prediction == 0 else "Dropout"
    print(f"Student {idx + 1}: Prediction = {label} ({prediction})")
