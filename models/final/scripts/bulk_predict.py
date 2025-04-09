import os
import sys
import pandas as pd

# === Setup Paths ===
FINAL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(FINAL_DIR, ".."))
sys.path.append(PROJECT_ROOT)

from utils.predictor import predict_new_data  # ✅ Now import works correctly

# === Path Constants ===
MODEL_PATH = os.path.join(FINAL_DIR, "artifacts/random_forest_model.pkl")
PREPROCESSED_DATA_PATH = os.path.join(FINAL_DIR, "data/preprocessed/preprocessed_enrolled_pupils.csv")
ALIGNED_ENROLLED_DATA_PATH = os.path.join(FINAL_DIR, "data/refined/aligned_enrolled_pupils.csv")
OUTPUT_PATH = os.path.join(FINAL_DIR, "data/results/enrolled_predictions.csv")

# === Run Prediction ===
try:
    predictions = predict_new_data(
        model_path=MODEL_PATH,
        data_path=PREPROCESSED_DATA_PATH,
        output_path=OUTPUT_PATH
    )
except Exception as e:
    print(f"❌ Error during prediction: {e}")
    sys.exit(1)

# === Load Datasets ===
try:
    aligned_enrolled_df = pd.read_csv(ALIGNED_ENROLLED_DATA_PATH)
    predictions_df = pd.read_csv(OUTPUT_PATH)
except Exception as e:
    print(f"❌ Error loading datasets: {e}")
    sys.exit(1)

# === Validate Record Count ===
if len(predictions_df) != len(aligned_enrolled_df):
    print(f"❌ ERROR: Prediction count ({len(predictions_df)}) does not match enrolled records ({len(aligned_enrolled_df)})!")
    sys.exit(1)

# === Merge + Label Predictions ===
aligned_enrolled_df["Predicted Outcome"] = predictions_df["Predicted Outcome"]
aligned_enrolled_df["Predicted Label"] = aligned_enrolled_df["Predicted Outcome"].map({1: "Graduate", 0: "Dropout"})

# === Save Final Dataset ===
try:
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    aligned_enrolled_df.to_csv(OUTPUT_PATH, index=False)
except Exception as e:
    print(f"❌ Error saving output: {e}")
    sys.exit(1)

# === Log Summary ===
total_students = len(aligned_enrolled_df)
total_graduates = (aligned_enrolled_df["Predicted Outcome"] == 1).sum()
total_dropouts = (aligned_enrolled_df["Predicted Outcome"] == 0).sum()

print(f"✅ Final predictions saved with original enrolled data: {OUTPUT_PATH}")
print("📊 Prediction Summary:")
print(f"   • Total Students:        {total_students}")
print(f"   • Predicted Graduates:   {total_graduates}")
print(f"   • Predicted Dropouts:    {total_dropouts}")
