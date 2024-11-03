import pandas as pd
import joblib
import os

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load the trained model, scalers, and feature names
model = joblib.load(os.path.join(base_dir, 'models', 'dropout_predictor_model.joblib'))
scaler = joblib.load(os.path.join(base_dir, 'models', 'scaler.joblib'))
min_max_scaler = joblib.load(os.path.join(base_dir, 'models', 'min_max_scaler.joblib'))
feature_names = joblib.load(os.path.join(base_dir, 'models', 'feature_names.joblib'))
numerical_columns = joblib.load(os.path.join(base_dir, 'models', 'numerical_columns.joblib'))

# Load and preprocess the sample data
sample = pd.read_csv(os.path.join(base_dir, 'data', 'sample_input_for_dropout_prediction.csv'))

# Print each column name with its corresponding value
for column in sample.columns:
    print(f"{column}: {sample[column].values[0]}")

# Apply the same preprocessing as in training
sample[['Age at enrollment']] = min_max_scaler.transform(sample[['Age at enrollment']])
sample[numerical_columns] = scaler.transform(sample[numerical_columns])

# Reindex to ensure columns match the original feature order
sample = sample.reindex(columns=feature_names, fill_value=0)

# Make prediction
prediction = model.predict(sample)

# Output the prediction
print("Prediction (0 = Graduate, 1 = Dropout):", prediction[0])
