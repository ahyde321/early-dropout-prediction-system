import os
import pandas as pd
import joblib

# Define paths
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
test_data_path = os.path.join(base_dir, 'data', 'test', 'preprocessed_high_risk_students.csv')
feature_names_path = os.path.join(base_dir, 'models', 'feature_names.joblib')

# Load the model's feature names and test data
print("Loading feature names and test data...")
feature_names = joblib.load(feature_names_path)
test_data = pd.read_csv(test_data_path)

# Compare features
print("Comparing features...")
test_columns = set(test_data.columns)
model_features = set(feature_names)

# Identify missing and extra features
missing_features = model_features - test_columns
extra_features = test_columns - model_features

# Output results
print("\n=== Comparison Results ===")
print(f"Total features expected by the model: {len(model_features)}")
print(f"Total features in the test data: {len(test_columns)}")
print(f"Missing features in test data: {len(missing_features)}")
print(f"Extra features in test data: {len(extra_features)}")

if missing_features:
    print("\nMissing features:")
    print(missing_features)
else:
    print("\nNo missing features in test data.")

if extra_features:
    print("\nExtra features (present in test data but not used by the model):")
    print(extra_features)
else:
    print("\nNo extra features in test data.")

# Automate test data alignment
print("\nAligning test data with model features...")
# Add missing features with default value 0
for feature in missing_features:
    test_data[feature] = 0

# Drop extra features
if extra_features:
    test_data = test_data.drop(columns=extra_features)

# Reorder columns to match the model's feature order
test_data = test_data[list(feature_names)]

# Save the aligned test data
aligned_test_data_path = os.path.join(base_dir, 'data', 'test', 'aligned_high_risk_students.csv')
test_data.to_csv(aligned_test_data_path, index=False)
print(f"\nAligned test data saved to: {aligned_test_data_path}")
