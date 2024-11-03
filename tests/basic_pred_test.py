import pandas as pd
import joblib
import os

# Load the trained model, scalers, and feature names
model = joblib.load(os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib'))
scaler = joblib.load(os.path.join(base_dir, 'models', 'scaler.joblib'))
min_max_scaler = joblib.load(os.path.join(base_dir, 'models', 'min_max_scaler.joblib'))
feature_names = joblib.load(os.path.join(base_dir, 'models', 'feature_names.joblib'))

# Load and preprocess the sample data
sample = pd.read_csv(os.path.join(base_dir, 'data', 'sample_input_for_dropout_prediction.csv'))

# Apply the same preprocessing as in training
sample[['Age at enrollment']] = min_max_scaler.transform(sample[['Age at enrollment']])
sample[numerical_columns] = scaler.transform(sample[numerical_columns])

# Reindex to ensure columns match the original feature order
sample = sample.reindex(columns=feature_names, fill_value=0)

# Make prediction
prediction = model.predict(sample)

# Output the prediction
print("Prediction (0 = Graduate, 1 = Dropout):", prediction[0])
