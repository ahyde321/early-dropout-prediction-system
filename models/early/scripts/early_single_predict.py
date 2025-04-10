import os
import sys
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler

# === Setup Paths ===
FINAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(FINAL_DIR, ".."))
sys.path.append(PROJECT_ROOT)

# === Load Early Model Artifacts ===
ARTIFACTS_DIR = os.path.join(FINAL_DIR, "artifacts")
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "random_forest_model.pkl")

with open(os.path.join(ARTIFACTS_DIR, "label_encoders.pkl"), "rb") as f:
    encoders = pickle.load(f)
with open(os.path.join(ARTIFACTS_DIR, "scaler.pkl"), "rb") as f:
    scaler = pickle.load(f)
with open(os.path.join(ARTIFACTS_DIR, "feature_names.pkl"), "rb") as f:
    feature_names = pickle.load(f)

# === Define Early-Stage Student Input ===
student_data = {
    "student_number": "b2cecdc4",
    "first_name": "Gary",
    "last_name": "Savage",
    "age_at_enrollment": 90,
    "application_order": 1,
    "curricular_units_1st_sem_enrolled": 6,
    "daytime_evening_attendance": 1,
    "debtor": 0,
    "displaced": 0,
    "gender": 0,
    "marital_status": 0,
    "scholarship_holder": 0,
    "tuition_fees_up_to_date": 1
}

# === Convert to DataFrame ===
student_df = pd.DataFrame([student_data])

# === Fill any missing features with 0 ===
for col in feature_names:
    if col not in student_df.columns:
        student_df[col] = 0

# ✅ Reorder columns to match training set
student_df = student_df[feature_names]

# === Encode Categorical Features ===
for col, le in encoders.items():
    if col in student_df.columns:
        student_df[col] = student_df[col].astype(str).map(lambda x: x if x in le.classes_ else "__unknown__")
        if "__unknown__" not in le.classes_:
            le.classes_ = list(le.classes_) + ["__unknown__"]
        student_df[col] = le.transform(student_df[col])

# === Scale Numerical Features ===
num_cols = student_df.select_dtypes(include=["int64", "float64"]).columns.tolist()
if scaler and num_cols:
    student_df[num_cols] = scaler.transform(student_df[num_cols])

# Final alignment
for col in feature_names:
    if col not in student_df.columns:
        student_df[col] = 0
student_df = student_df[feature_names]

# === Run Prediction ===
try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    prediction = model.predict(student_df)[0]
    probability = model.predict_proba(student_df)[0][1]  # Probability of class 1 (Graduate)
    prediction_label = "Graduate" if prediction == 1 else "Dropout"
    risk_score = 1 - probability  # Higher = higher risk of dropout

    # Risk bucket
    if risk_score >= 0.8:
        rating = "Very High Risk"
    elif risk_score >= 0.6:
        rating = "High Risk"
    elif risk_score >= 0.4:
        rating = "Moderate Risk"
    elif risk_score >= 0.2:
        rating = "Low Risk"
    else:
        rating = "Very Low Risk"

except Exception as e:
    print(f"❌ Prediction error: {e}")
    sys.exit(1)

# === Display Output ===
print("\n✅ Early-Semester Prediction for student:")
for key, value in student_data.items():
    print(f"   • {key.replace('_', ' ').capitalize()}: {value}")

print(f"\n🧠 Predicted Outcome: {prediction_label} ({prediction})")
print(f"📊 Risk Score: {risk_score:.2f} → {rating}")
