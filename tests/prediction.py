import sys
import os
import joblib
import pandas as pd

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_dir)

input_file = os.path.join(base_dir, 'data', 'test', 'enrolled_dataset.csv')
model_file = os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib')
feature_names_file = os.path.join(base_dir, 'models', 'feature_names.joblib')
output_file = os.path.join(base_dir, 'data', 'results', 'enrolled_student_predictions.csv')
raw_enrolled = os.path.join(base_dir, 'data', 'test', 'raw_enrolled_dataset.csv')

print("Loading the trained model and feature names...")
model = joblib.load(model_file)
feature_names = joblib.load(feature_names_file)
print("Model and feature names loaded successfully.")

print("Loading the preprocessed data...")
preprocessed_data = pd.read_csv(input_file)
raw_data = pd.read_csv(raw_enrolled)  # Load the raw enrolled data

print("Aligning data with the model's feature names...")
for feature in feature_names:
    if feature not in preprocessed_data.columns:
        preprocessed_data[feature] = 0  # Add missing features with default value

preprocessed_data = preprocessed_data[feature_names]  # Ensure column order matches

print("Making predictions...")
predictions = model.predict(preprocessed_data)
probabilities = model.predict_proba(preprocessed_data)

results = pd.DataFrame({
    "Prediction": ["High Risk (Dropout)" if prob[1] > 0.9 else "Likely Graduate" for prob in probabilities],
    "Dropout Risk": [prob[1] for prob in probabilities],
    "Graduate Probability": [prob[0] for prob in probabilities]
})

# Combine raw data with predictions
final_results = pd.concat([raw_data.reset_index(drop=True), results.reset_index(drop=True)], axis=1)

os.makedirs(os.path.dirname(output_file), exist_ok=True)
final_results.to_csv(output_file, index=False)

print(f"Predictions with raw data saved to {output_file}")

print("\nPredictions for enrolled students:")
for idx, row in final_results.iterrows():
    print(f"Student {idx + 1}: Prediction = {row['Prediction']} (Dropout Risk: {row['Dropout Risk']:.2f}, Graduate Probability: {row['Graduate Probability']:.2f})")

print("Prediction process completed.")
