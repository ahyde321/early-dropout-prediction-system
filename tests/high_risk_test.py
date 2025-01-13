import sys
import os
import pandas as pd
import joblib

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

from pipeline.preprocess_td import preprocess_test_data

# Define the paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
input_file = os.path.join(base_dir, 'data', 'raw', 'high_risk_student_dataset.csv')
preprocessed_output_file = os.path.join(base_dir, 'data', 'test', 'preprocessed_high_risk_students.csv')
model_file = os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib')
feature_names_file = os.path.join(base_dir, 'models', 'feature_names.joblib')


model = joblib.load(model_file)
feature_names = joblib.load(feature_names_file)



# Preprocess the data
preprocess_test_data(
    input_file=input_file,
    output_file=preprocessed_output_file,
)

preprocessed_data = pd.read_csv(preprocessed_output_file)

predictions = model.predict(preprocessed_data)

print("\nPredictions for each student (0 = Graduate, 1 = Dropout):")
for idx, prediction in enumerate(predictions):
    print(f"Student {idx + 1}: Prediction = {prediction}")
