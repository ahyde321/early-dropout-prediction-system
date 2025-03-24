import os
import sys
import pandas as pd

# Get the absolute path of the project root directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from utils.predictor import predict_new_data

# Paths
MODEL_PATH = os.path.join(BASE_DIR, "models/random_forest_model.pkl")  # ✅ Uses the trained Random Forest model
PREPROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data/preprocessed/preprocessed_enrolled_pupils.csv")  # ✅ Preprocessed enrolled dataset
ALIGNED_ENROLLED_DATA_PATH = os.path.join(BASE_DIR, "data/refined/aligned_enrolled_pupils.csv")  # ✅ Original enrolled dataset (before preprocessing)
OUTPUT_PATH = os.path.join(BASE_DIR, "data/results/enrolled_predictions.csv")  # ✅ Final output file with predictions

# ✅ Run predictions on the enrolled dataset
predictions = predict_new_data(
    model_path=MODEL_PATH,
    data_path=PREPROCESSED_DATA_PATH,
    output_path=OUTPUT_PATH  # ✅ Save the predictions
)

# ✅ Load the original enrolled dataset
aligned_enrolled_df = pd.read_csv(ALIGNED_ENROLLED_DATA_PATH)

# ✅ Load the saved predictions
predictions_df = pd.read_csv(OUTPUT_PATH)

# ✅ Ensure predictions and original data have the same number of records
if len(predictions_df) != len(aligned_enrolled_df):
    print(f"❌ ERROR: Prediction count ({len(predictions_df)}) does not match enrolled records ({len(aligned_enrolled_df)})!")
    sys.exit(1)

# ✅ Merge predictions with the original enrolled dataset
aligned_enrolled_df["Predicted Outcome"] = predictions_df["Predicted Outcome"]

# ✅ Optional: Map to readable labels
aligned_enrolled_df["Predicted Label"] = aligned_enrolled_df["Predicted Outcome"].map({1: "Graduate", 0: "Dropout"})

# ✅ Save the final dataset with predictions
aligned_enrolled_df.to_csv(OUTPUT_PATH, index=False)

# ✅ Log prediction counts
total_students = len(aligned_enrolled_df)
total_graduates = (aligned_enrolled_df["Predicted Outcome"] == 1).sum()
total_dropouts = (aligned_enrolled_df["Predicted Outcome"] == 0).sum()

print(f"✅ Final predictions saved with original enrolled data: {OUTPUT_PATH}")
print("📊 Prediction Summary:")
print(f"   • Total Students:  {total_students}")
print(f"   • Predicted Graduates: {total_graduates}")
print(f"   • Predicted Dropouts:  {total_dropouts}")