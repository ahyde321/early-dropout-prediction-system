import sys
import os
import joblib
import pandas as pd
import numpy as np

# Define paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

input_file = os.path.join(base_dir, 'data', 'enrolled', 'preprocessed_enrolled.csv')
model_file = os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib')
feature_names_file = os.path.join(base_dir, 'models', 'feature_names.joblib')
threshold_file = os.path.join(base_dir, 'models', 'optimal_threshold.joblib')
output_file = os.path.join(base_dir, 'data', 'results', 'enrolled_student_predictions.csv')
raw_enrolled = os.path.join(base_dir, 'data', 'enrolled', 'raw_enrolled.csv')

# Define label mapping
REVERSE_LABEL_MAP = {0: "Likely Graduate", 1: "High Risk (Dropout)"}

# Load model, feature names, and threshold
print("\n🔄 Loading the trained model, feature names, and optimal threshold...")
model = joblib.load(model_file)
feature_names = joblib.load(feature_names_file)
optimal_threshold = joblib.load(threshold_file)
print("✅ Model, feature names, and optimal threshold loaded successfully.")

# Load the preprocessed and raw data
preprocessed_data = pd.read_csv(input_file)
raw_data = pd.read_csv(raw_enrolled)

# Ensure all expected features exist in the dataset
missing_features = [feature for feature in feature_names if feature not in preprocessed_data.columns]
if missing_features:
    # Ensure only numeric columns are used for median imputation
    numeric_medians = preprocessed_data.select_dtypes(include=[np.number]).median()
    for feature in missing_features:
        preprocessed_data[feature] = numeric_medians.get(feature, 0)

# Ensure correct feature order
preprocessed_data = preprocessed_data[feature_names]  

# Make predictions
probabilities = model.predict_proba(preprocessed_data)
predicted_classes = (probabilities[:, 1] > optimal_threshold).astype(int)

# Map predictions to labels
predicted_labels = [REVERSE_LABEL_MAP[pred] for pred in predicted_classes]

# Create results DataFrame
results = pd.DataFrame({
    "Prediction": predicted_labels,
    "Dropout Risk": probabilities[:, 1],
    "Graduate Probability": probabilities[:, 0]
})

# Combine raw data with predictions
final_results = pd.concat([raw_data.reset_index(drop=True), results.reset_index(drop=True)], axis=1)

# Save predictions to file
os.makedirs(os.path.dirname(output_file), exist_ok=True)
final_results.to_csv(output_file, index=False)

print(f"\n✅ Predictions saved to: {output_file}")

# Print summary
summary_counts = results['Prediction'].value_counts()
print("\n📊 Dropout Risk Predictions Summary:")
print(f"✔ Likely Graduates: {summary_counts.get('Likely Graduate', 0)} students")
print(f"⚠️ High Risk (Dropout): {summary_counts.get('High Risk (Dropout)', 0)} students")

print("\n🎯 Dropout Risk Assessment Completed Successfully!")
