import os
import sys
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler

# === Setup Paths ===
FINAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(FINAL_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from utils.predictor import predict_new_data  # ✅ Uses the same utility as batch prediction

# === Load Preprocessing Artifacts ===
ARTIFACTS_DIR = os.path.join(FINAL_DIR, "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "random_forest_model.pkl")

with open(os.path.join(ARTIFACTS_DIR, "label_encoders.pkl"), "rb") as f:
    encoders = pickle.load(f)
with open(os.path.join(ARTIFACTS_DIR, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)
with open(os.path.join(ARTIFACTS_DIR, "feature_names.pkl"), "rb") as f:
    feature_names = pickle.load(f)

# === Define a single student input (🧠 Easily editable block) ===
student_data = {
  "student_number": "dcac096b",
  "first_name": "Alice",
  "last_name": "Smith",
  "age_at_enrollment": 18,
  "curricular_units_1st_sem_enrolled": 6,
  "debtor": 0,
  "displaced": 1,
  "gender": 0,
  "scholarship_holder": 0,
  "tuition_fees_up_to_date": 1,
  "curricular_units_1st_sem_approved": 6,
  "curricular_units_1st_sem_grade": 14,
  "curricular_units_2nd_sem_grade": 14
}

# Convert to DataFrame
# Turn your hardcoded dictionary into a DataFrame
student_df = pd.DataFrame([student_data])

# Fill any missing features with 0 (if not in student_data)
for col in feature_names:
    if col not in student_df.columns:
        student_df[col] = 0

# ✅ Reorder columns to match the training set exactly
student_df = student_df[feature_names]

# Encode categorical columns
for col, le in encoders.items():
    if col in student_df.columns:
        student_df[col] = student_df[col].astype(str).map(lambda x: x if x in le.classes_ else "__unknown__")
        if "__unknown__" not in le.classes_:
            le.classes_ = list(le.classes_) + ["__unknown__"]
        student_df[col] = le.transform(student_df[col])

# Scale numeric columns
num_cols = student_df.select_dtypes(include=["int64", "float64"]).columns.tolist()
if scaler and num_cols:
    student_df[num_cols] = scaler.transform(student_df[num_cols])

# Align columns
for col in feature_names:
    if col not in student_df.columns:
        student_df[col] = 0
student_df = student_df[feature_names]

# === Run Prediction ===
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    prediction = model.predict(student_df)[0]
    prediction_label = "Graduate" if prediction == 1 else "Dropout"
except Exception as e:
    print(f"❌ Prediction error: {e}")
    sys.exit(1)

# === Display Result ===
print("\n✅ Prediction for single student:")
for key, value in student_data.items():
    print(f"   • {key.replace('_', ' ').capitalize()}: {value}")

print(f"\n🧠 Predicted Outcome: {prediction_label} ({prediction})")